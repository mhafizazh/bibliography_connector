from bibliography_connector.transforms.clean import clean_items
from bibliography_connector.transforms.remdup import remdup_items

def run_pipeline(raw_items):
    items = clean_items(raw_items)
    items = remdup_items(items)

    return items