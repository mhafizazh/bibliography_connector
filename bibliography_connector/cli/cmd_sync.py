import typer
import os
from rich import print
from bibliography_connector.providers.zotero import ZoteroProvider
# from dateutil.parser import parse
from datetime import date
from bibliography_connector.exporters.hugo import HugoExporter


sync_app = typer.Typer(help="Sync bibliography from Zotero")


# @sync_app.callback()
def _run_sync(raw_items, outdir, suffix=""):
    # items = run_pipeline(raw_items) # this should returned cleaned items
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
    

    # import json
    # with open("debug_raw.json", "w") as f:
    #     json.dump(raw_items, f, indent=2)

    print(f"Fetched {len(provider.cleaned_items)} items")
    # print(provider.cleaned_items)
    _run_sync(provider.cleaned_items, output)

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
    provider.fetch(q=str(year), qmode="titleCreatorYear")
    print(f"Fetched {len(provider.cleaned_items)} items")
    
    filtered = [i for i in provider.cleaned_items if isinstance(i.get("date"), date) and i["date"].year == year]
    print(f"Filtered down to {len(filtered)} items for year {year}")
    _run_sync(filtered, output, suffix=f"_{year}")


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

    from dateutil import parser as dateparser

    target = dateparser.parse(date_str).date()

    provider.fetch(q=str(target.year), qmode="titleCreatorYear")
    print(f"Fetched {len(provider.cleaned_items)} items")
    
    filtered = [i for i in provider.cleaned_items if isinstance(i.get("date"), date) and i["date"] == target]
    # for i in provider.cleaned_items:  
    #     print(f"  date={i.get('date')!r}, type={type(i.get('date')).__name__}")

    print(f"Filtered down to {len(filtered)} items for year {target}")
    _run_sync(filtered, output, suffix=f"_{target}")