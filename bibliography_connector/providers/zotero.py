import httpx

class ZoteroProvider:
    def __init__(self, group_id, collection):
        self.group_id = group_id
        self.collection = collection

    def fetch(self):
        # main entry point fetch all items from Zotero inside group and collection
        all_items = [] # item object in zotero
        all_collections = [] # collection object in zotero
        root_meta = self.get_zotero(f"groups/{self.group_id}/collections/{self.collection}")
        all_collections.append(self.merge(root_meta))

        self.fetch_collection_reccursive(self.collection, all_items, all_collections)

        all_keys = {item["key"] for item in all_items}
        uncollected = self.fetch_uncollected_items(all_keys)
        all_items.extend(uncollected)

        return {
            "items": all_items,
            "collections": all_collections
        }
    
    def fetch_collection_recursive(self, collection_key, all_items, all_collections):
        collection = self.get_zotero(f"groups/{self.group_id}/collections/{collection_key}")
        collection_name = collection.get('data', {}).get('name', 'Unknown')
        deleted = collection.get('data', {}).get('deleted', False)
        num_items = collection.get('meta', {}).get('numItems', 0)

        if deleted:
            print(f"skipping deleted collection {collection_key}: {collection_name}")
            return
        
        all_collections.append(collection)

        if num_items == 0:
            print(f"Empty collection {collection_key}: {collection_name}")
        else:
            print(f"getting collection {collection_key}: {collection_name}")

        start = 0
        limit = 100
        while True:
            items = self.get_zotero(f"groups/{self.group_id}/collections/{collection_key}/items"
            f"?start={start}&limit={limit}"
            )
            if items:
                all_items.extend(items)
                start += len(items)
            else:
                break
            if len(items) < limit:
                break
        
        # fetch child collection and recurse it 
        subcollections = self.get_zotero(f"groups/{self.group_id}/collections/{collection_key}/collections")
        if subcollections:
            for sub in subcollections:
                all_collections.append(sub)

            for subcollection in subcollections:
                child_key = subcollection.get('key')
                if child_key:
                    self.fetch_collection_recursive(child_key, all_items, all_collections)


    def fetch_uncollected_items(self, existing_keys):
        pass

    def api(self, path):
        pass

    def merge(self, obj):
        # flattens zotero api into one dictionary
        merged = {}
        # some flattent loop
        return merged

    def get_zotero(self, path):
        response = httpx.get(f"https://api.zotero.org/{path}")
        response.raise_for_status()
        return response.json()