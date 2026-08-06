from bibliography_connector.providers.zotero import ZoteroProvider   
import unittest
import json
from pathlib import Path
from bibliography_connector.providers.zotero import ZoteroProvider

FIXTURES = json.loads((Path(__file__).parent / "example.json").read_text())

class TestZoteroProvider(unittest.TestCase):
    def setUp(self):
        self.provider = ZoteroProvider("6588052", "J2TGC2ZT")
        self.provider.fetch(items=FIXTURES)

    def test_clean_fields_removes_empties(self):
        """using first value in example.json has all fields empty"""
        # self.provider._clean_fields()
        item = self.provider.cleaned_items[0]
        self.assertNotIn("date", item)
        self.assertNotIn("abstractNote", item)
        self.assertIn("title", item)

    def test_clean_fields_parses_edtf_date(self):
        """2nd item has date='2026-03-20' and check if its converted to edtf date object"""
        # self.provider._clean_fields()
        from edtf.parser.parser_classes import Date
        self.assertIsInstance(self.provider.cleaned_items[1]["date"], Date) # check if its edtf date object
        self.assertEqual(int(self.provider.cleaned_items[1]["date"].year), 2026)

    def test_url_consolidate_doi_fallback(self):
        doi_item = next(i for i in self.provider.cleaned_items if i.get("DOI"))
        self.assertEqual(doi_item["url"], "https://doi.org/10.1234/test")

    def test_url_consolidate_child_url(self):
        parent = next(i for i in self.provider.cleaned_items if i.get("key") == "PARENT1")
        self.assertEqual(parent["url"], "https://child.com")
        self.assertFalse(any("parentItem" in i for i in self.provider.cleaned_items))
        self.assertEqual(len(self.provider.cleaned_items), 5)

    def test_filter_by_date_year(self):
        from edtf.parser.parser_classes import Date
        # self.provider._clean_fields()
        result = ZoteroProvider.filter_by_date(
            self.provider.cleaned_items, Date(2026, 1, 1), "year")
        self.assertEqual(len(result), 2)  # both have 2026 dates


    def test_fetch_uses_fixture(self):
        self.assertEqual(self.provider.items, FIXTURES)
        self.assertEqual(len(self.provider.cleaned_items), 5)