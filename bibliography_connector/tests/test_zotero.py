from bibliography_connector.providers.zotero import ZoteroProvider
from rich import print
import json

def test_manual():
    # 1. Setup
    group_id = "2914042"  # Or a test one
    collection = "FSK5IX4F"
    provider = ZoteroProvider(group_id, collection)

    print("--- Testing Merge Logic ---")
    sample_data = {
        "key": "123", 
        "data": {"title": "Test Paper"}, 
        "meta": {"numChildren": 0}
    }
    merged = provider.merge(sample_data)
    print(f"Merged Result: {merged}")

    print("\n--- Testing API Connection ---")
    try:
        # Just test one small call to see if your auth/path works
        data = provider.get_zotero(f"groups/{group_id}/collections/{collection}")
        print("Success! Data received from Zotero.")
        print(f"Collection Name: {data.get('data', {}).get('name')}")
        print(f"DEBUG {json.dumps(data, indent=2)}")
        print(f"Collection Name: {data.get('data', {}).get('name')}")
    except Exception as e:
        print(f"API Call Failed: {e}")

    print("\n--- Testing Full Fetch ---")
    # Warning: This will actually hit the API and count against rate limits
    # results = provider.fetch()
    # print(f"Found {len(results['items'])} items.")

def test_fetch_collection_recursive():
    group_id = "2914042"
    collection = "FSK5IX4F"
    provider = ZoteroProvider(group_id, collection)
    all_items = []
    all_collections = []
    try:
        provider.fetch_collection_recursive(collection, all_items, all_collections)
        
        print(f"=== DEBUG: Collections found: {len(all_collections)} ===")
        for i, col in enumerate(all_collections):
            print(f"\n[Collection {i+1}]")
            print(f"  Key: {col.get('key')}")
            print(f"  Name: {col.get('data', {}).get('name')}")
            print(f"  numItems: {col.get('meta', {}).get('numItems')}")
            print(f"  Child Collections: {col.get('data', {}).get('collections', [])}")
        
        print(f"\n=== DEBUG: Items found: {len(all_items)} ===")
        for i, item in enumerate(all_items[:5]):  # Show first 5 items
            print(f"\n[Item {i+1}]")
            print(f"  Key: {item.get('key')}")
            print(f"  Title: {item.get('data', {}).get('title', 'N/A')}")
            print(f"  Type: {item.get('data', {}).get('itemType', 'N/A')}")
            print(f"  Year: {item.get('data', {}).get('date', 'N/A')}")
            print(f"  JSON: {json.dumps(item.get('data', {}), indent=4)}")
        
        # if len(all_items) > 5:
        #     print(f"\n... and {len(all_items) - 5} more items")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_manual()
    test_fetch_collection_recursive()
