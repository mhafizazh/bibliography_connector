import click
from pyzotero import Zotero
import json


@click.command(name="get_item")
@click.option(
    "--group",
    required=True,
    help="group id identification number"
)
def get_item(group):
    zot = Zotero(
        library_id=group, 
        library_type="group"
    )
    items = zot.everything(zot.top())
    json_string = json.dumps(items, indent=4)
    print(json_string)
    num = 0
    print(f"Total items retrieved: {len(items)}")
    print(type(items))
    # Define the output filename
    output_filename = "zotero_items.json"
    
    # Save the data to a JSON file
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)
        
    click.echo(f"Successfully saved {len(items)} items to {output_filename}")