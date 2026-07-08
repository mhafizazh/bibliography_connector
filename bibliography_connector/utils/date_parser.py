import re
from datetime import date

MONTH_NAMES = {
    'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
    'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
    'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
    'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
    'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
    'dec': 12, 'december': 12,
}

def parse_date_input(date_str):
    date_str = date_str.strip()

    # full date: YYYY-MM-DD or YYYY/MM/DD
    m = re.match(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', date_str)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3))), "day"

    # Year-month: YYYY-MM or YYYY/MM
    m = re.match(r'^(\d{4})[-/](\d{1,2})$', date_str)
    if m:
        return date(int(m.group(1)), int(m.group(2)), 1), "month"

    # Year only: YYYY
    m = re.match(r'^(\d{4})$', date_str)
    if m:
        return date(int(m.group(1)), 1, 1), "year"

    # Month YYYY
    m = re.match(r'^([a-zA-Z]+)\s+(\d{4})$', date_str)
    if m:
        month = MONTH_NAMES.get(m.group(1).lower())
        if month:
            return date(int(m.group(2)), month, 1), "month"

    # YYYY Month
    m = re.match(r'^(\d{4})\s+([a-zA-Z]+)$', date_str)
    if m:
        month = MONTH_NAMES.get(m.group(2).lower())
        if month:
            return date(int(m.group(1)), month, 1), "month"

    # DD Month YYYY
    m = re.match(r'^(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})$', date_str)
    if m:
        month = MONTH_NAMES.get(m.group(2).lower())
        if month:
            return date(int(m.group(3)), month, int(m.group(1))), "day"

    # Month DD, YYYY or Month DD YYYY
    m = re.match(r'^([a-zA-Z]+)\s+(\d{1,2}),?\s+(\d{4})$', date_str)
    if m:
        month = MONTH_NAMES.get(m.group(1).lower())
        if month:
            return date(int(m.group(3)), month, int(m.group(2))), "day"

    raise ValueError(f"Cannot parse date: {date_str}")
