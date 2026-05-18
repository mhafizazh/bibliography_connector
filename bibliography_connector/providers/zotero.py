from pyzotero import Zotero

class ZoteroProvider:
    def __init__(self, group_id, collection):
        self.group_id = group_id
        self.collection = collection

    def fetch(self):
        zot = Zotero(library_id=self.group_id, library_type="group")
        items = zot.everything(zot.top())
        return items