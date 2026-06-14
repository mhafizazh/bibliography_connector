from pyzotero import Zotero

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

    def _semiflatten(self):
        pass 
    
    def _clean_fields(self):
        pass
    
    def _remdup(self):
        pass

    def _url_consolidate(self):

    def _clean_abstract(self):
        pass
    
    def _add_date_strings(self):
        pass
    
    def _add_author_strings(self):
        pass

        
    def fetch(self, **kwargs):
        self.items = self._fetch_items(self.collection, **kwargs)

    def transform(self):
        pass