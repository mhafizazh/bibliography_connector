import httpx
from pyzotero import Zotero

class ZoteroProvider:
    def __init__(self, group_id, collection):
        self.group_id = group_id
        self.collection = collection

    def fetch(self):
        zot = Zotero(library_id=self.group_id, library_type="group")
        items = zot.everything(zot.top())
        print(f"Total bibliography items retrieved: {len(items)}")
        return items
        # json_string = json.dumps(items, indent=4)
        # print(json_string)
        # num = 0
        # print(f"Total items retrieved: {len(items)}")
        # print(type(items))
        # # Define the output filename
        # output_filename = "zotero_items.json"
        
        # # Save the data to a JSON file
        # with open(output_filename, "w", encoding="utf-8") as f:
        #     json.dump(items, f, indent=4, ensure_ascii=False)
            
        # click.echo(f"Successfully saved {len(items)} items to {output_filename}")