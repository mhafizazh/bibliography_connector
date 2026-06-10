import typer
import os
from rich import print
from bibliography_connector.providers.zotero import ZoteroProvider
from bibliography_connector.transforms.clean import clean_items
from bibliography_connector.transforms.remdup import remdup_items
from bibliography_connector.exporters.hugo import HugoExporter

# app = typer.Typer(help="Bibliography connector CLI")

sync_app = typer.Typer(help="Sync bibliography from Zotero")
# app.add_typer(sync_app, name="sync")

# @sync_app.callback()
def _run_sync(raw_items, outdir, suffix=""):
    items = clean_items(raw_items)
    items = remdup_items(items)
    print(f"Processed {len(items)} items")
    HugoExporter(
        output_dir=outdir,
        json_file=os.path.join(outdir, f"bibliography{suffix}.json"),
    ).export(items)

@sync_app.command("all")
def sync_all(
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")     
):
    print("[cyan]Fetching bibliography...[/cyan]")
    provider = ZoteroProvider(group_id=groupid, collection=collection)
    raw_items = provider.fetch()

    # import json
    # with open("debug_raw.json", "w") as f:
    #     json.dump(raw_items, f, indent=2)

    print(f"Fetched {len(raw_items)} items")
    _run_sync(raw_items, output)

@sync_app.command("year")
def sync_by_year(
    year: int = typer.Argument(..., help="Publication year to filter by"),
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")     
):
    """Sync bibliography for a specific publication year"""
    print("Fetching bibliography...")
    provider = ZoteroProvider(group_id=groupid, collection=collection)
    raw_items = provider.fetch(q=str(year), qmode="titleCreatorYear")
    filtered = [i for i in raw_items if str(year) in (i.get("data", {}).get("date") or "")]
    print(f"Fetched {len(filtered)} items")
    _run_sync(filtered, output, suffix=f"_{year}")