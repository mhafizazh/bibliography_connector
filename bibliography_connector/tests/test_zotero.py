from bibliography_connector.providers.zotero import ZoteroProvider
from rich import print
import json

def test_fetch_collection_recursive():
    group_id = "2914042"
    collection = "FSK5IX4F"
    provider = ZoteroProvider(group_id, collection)
    all_items = []
    all_collections = []
    try:
        ret = provider.fetch()
        print(ret)   
        
        # if len(all_items) > 5:
        #     print(f"\n... and {len(all_items) - 5} more items")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_collection_recursive()
