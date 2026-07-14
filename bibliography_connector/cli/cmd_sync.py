import typer
import os
from rich import print
from bibliography_connector.providers.zotero import ZoteroProvider
from datetime import date, datetime
from bibliography_connector.exporters.hugo import HugoExporter
from bibliography_connector.utils import parse_date_input



sync_app = typer.Typer(help="Sync bibliography from Zotero")


def _run_sync(raw_items, outdir, suffix=""):
    print(f"Processed {len(raw_items)} items")
    HugoExporter(
        output_dir=outdir,
        json_file=os.path.join(outdir, f"bibliography{suffix}.json"),
    ).export(raw_items)

@sync_app.command("all")
def sync_all(
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")
):
    print("[cyan]Fetching bibliography...[/cyan]")
    provider = ZoteroProvider(group_id=groupid, collection=collection)
    provider.fetch()
 
    print(f"Fetched {len(provider.cleaned_items)} items")
    _run_sync(provider.cleaned_items, output)



@sync_app.command("date")
def sync_by_date(
    date_str: str = typer.Argument(..., help="publication by date"),
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")
):
    """Sync bibliography for a specific publication date"""
    print("Fetching bibliography...")
    provider = ZoteroProvider(group_id=groupid, collection=collection)
    date, precision = parse_date_input(date_str)

    target = date

    provider.fetch(q=str(target.year), qmode="titleCreatorYear")
    print(f"Fetched {len(provider.cleaned_items)} items")

    filtered = ZoteroProvider.filter_by_date(provider.cleaned_items, target, precision)

    print(f"Filtered down to {len(filtered)}")
    _run_sync(filtered, output, suffix=f"_{target}")
