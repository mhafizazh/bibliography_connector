from bibliography_connector.providers.zotero import ZoteroProvider
from rich import print
import json

def test_fetch_collection_recursive():
    group_id = "6588052"
    collection = "J2TGC2ZT"
    bib_collection = ZoteroProvider(group_id, collection)
    all_items = []
    all_collections = []
    try:
        bib_collection.fetch()
        # print(type(bib_collection.items))   
        # for item in bib_collection.items:
        #     print(type(item))
        
        bib_collection.clean_fields()
        print(bib_collection.cleaned_items)
        
        # if len(all_items) > 5:
        #     print(f"\n... and {len(all_items) - 5} more items")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_collection_recursive()
