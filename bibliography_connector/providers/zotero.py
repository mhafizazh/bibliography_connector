from pyzotero import Zotero
from edtf import parse_edtf
from edtf.parser.edtf_exceptions import EDTFParseException
from edtf.parser.parser_classes import Date, UncertainOrApproximate
import logging 
import re
from bibliography_connector.utils.date_parser import parse_date_input

class ZoteroProvider:
    def __init__(self, group_id, collection):
        self.group_id = group_id
        self.collection = collection
        self.items = []
        self.cleaned_items = []

    def _fetch_items(self, collection_key, **kwargs):
        zot = Zotero(library_id=self.group_id, library_type="group")
        items = zot.everything(zot.collection_items_top(collection_key, **kwargs))
        for sub in zot.everything(zot.collections_sub(collection_key)):
            sub_key = sub.get("data", {}).get("key")
            if sub_key:
                items.extend(self._fetch_items(sub_key, **kwargs))
        return items
   
    def _clean_fields(self):
        """
        remove empty fields
        """
        for item in self.items:
            cleaned = {}
            for key, value in item["data"].items():
                if value == "" or value == None or value == [] or value == {} or value == '':
                    continue
                if key == 'date':
                    try:
                        value = parse_edtf(value)
                    except (EDTFParseException, ValueError, TypeError):
                        try:
                            value, _ = parse_date_input(value)
                        except ValueError:
                            logging.debug(f"Could not parse date {value}")
                cleaned[key] = value
            self.cleaned_items.append(cleaned)

    def _url_consolidate(self):
        """
        it will make URL lowercase, and if there is not URL use DOI url
        propagates child URLs up to parent item
        """
        for item in self.cleaned_items:
            url = item.get("url")
            doi = item.get("DOI")
            if url:
                item['url'] = url.lower()
            elif not url and doi:
                doi = doi.lstrip("/")
                item['url'] = f"https://doi.org/{doi}"
            
        child_urls = {}
        for item in self.cleaned_items:
            parent_key = item.get("parentItem")
            if parent_key and item.get("url"):
                if parent_key not in child_urls:
                    child_urls[parent_key] = item["url"]
        for item in self.cleaned_items:
            if not item.get("url") and item.get("key") in child_urls:
                item["url"] = child_urls[item["key"]]

        self.cleaned_items = [i for i in self.cleaned_items if "parentItem" not in i]


    def _clean_abstract(self):
        pass
    
    def _add_date_strings(self):
        pass
    
    def _add_author_strings(self):
        pass

    @staticmethod
    def filter_by_date(items, target_date, precision):
        def _get_date(item):
            d = item.get("date")
            if d is None:
                return None
            if isinstance(d, UncertainOrApproximate):
                d = d.date
            if isinstance(d, (Date)):
                return d
            return None

        def _match(edtf_date, td, prec):
            y = int(edtf_date.year)
            m = int(edtf_date.month) if edtf_date.month is not None else None
            d = int(edtf_date.day) if edtf_date.day is not None else None
            if prec == "day":
                return y == td.year and m == td.month and d == td.day
            elif prec == "month":
                return y == td.year and (m == td.month or m is None)
            else:
                return y == td.year

        results = []
        for item in items:
            edtf_date = _get_date(item)
            if edtf_date is not None and _match(edtf_date, target_date, precision):
                results.append(item)
        return results
            
    def fetch(self, **kwargs):
        self.items = self._fetch_items(self.collection, **kwargs)
        parent_keys = [item["data"]["key"] for item in self.items]
        self._clean_fields()
        self._url_consolidate()

    def transform(self):
        pass