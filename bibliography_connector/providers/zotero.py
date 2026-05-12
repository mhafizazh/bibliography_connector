import httpx

class ZoteroProvider:
    def __init__(self, group_id, collection):
        self.group_id = group_id
        self.root_collection = root_collection

    def fetch(self):
        url = (
            f"https://api.zotero.org/groups/"
            f"{self.group_id}/collections/"
            f"{self.collection}/items"
        )

        response = httpx.get(url)

        response.raise_for_status()

        return response.json()