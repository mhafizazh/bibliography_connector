from bibliography_connector.utils.date_parser import parse_date_input   
import unittest
from edtf.parser.parser_classes import Date
""" 
- parse_date_input function tests:
- YYYY-MM-DD → (Date, "day")
- YYYY-MM → (Date, "month")
- YYYY → (Date, "year")
- M/YYYY → (Date, "month")
- "Month YYYY" → (Date, "month")
- "DD Month YYYY" → (Date, "day")
- "Month DD, YYYY" → (Date, "day")
- Invalid format → ValueError
"""

class TestParseDateInput(unittest.TestCase):
    def test_full_date(self):
        self.assertEqual(parse_date_input("2023-08-15"), (Date(2023, 8, 15), "day"))
        self.assertEqual(parse_date_input("2023/08/15"), (Date(2023, 8, 15), "day"))

    def test_year_month(self):
        self.assertEqual(parse_date_input("2023-08"), (Date(2023, 8, 1), "month"))
        self.assertEqual(parse_date_input("2023/08"), (Date(2023, 8, 1), "month"))

    def test_year_only(self):
        self.assertEqual(parse_date_input("2023"), (Date(2023, 1, 1), "year"))

    def test_month_year(self):
        self.assertEqual(parse_date_input("8/2023"), (Date(2023, 8, None), "month"))
        self.assertEqual(parse_date_input("August 2023"), (Date(2023, 8, 1), "month"))
        self.assertEqual(parse_date_input("Aug 2023"), (Date(2023, 8, 1), "month"))
        self.assertEqual(parse_date_input("2023 August"), (Date(2023, 8, 1), "month"))
        self.assertEqual(parse_date_input("2023 Aug"), (Date(2023, 8, 1), "month"))

    def test_day_month_year(self):
        self.assertEqual(parse_date_input("15 August 2023"), (Date(2023, 8, 15), "day"))
        self.assertEqual(parse_date_input("15 Aug 2023"), (Date(2023, 8, 15), "day"))
        self.assertEqual(parse_date_input("August 15, 2023"), (Date(2023, 8, 15), "day"))
        self.assertEqual(parse_date_input("Aug 15, 2023"), (Date(2023, 8, 15), "day"))

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_date_input("invalid date")
    # TODO: Implement edge cases for invalid months, invalid days, leap years, etc.
    def test_invalid_month(self):
        pass