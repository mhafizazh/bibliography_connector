import typer
import os
from rich import print
from bibliography_connector.providers.zotero import ZoteroProvider
from bibliography_connector.pipeline import run_pipeline
from bibliography_connector.exporters.hugo import HugoExporter

# app = typer.Typer(help="Bibliography connector CLI")

sync_app = typer.Typer(help="Sync bibliography from Zotero")
# app.add_typer(sync_app, name="sync")

# @sync_app.callback()
def _run_sync(raw_items, outdir, suffix=""):
    items = run_pipeline(raw_items)
    print(f"[yellow]Processed {len(items)} items[/yellow]")
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
    print(f"[green]Fetched {len(raw_items)} items[/green]")
    _run_sync(raw_items, output)

@sync_app.command("year")
def sync_by_year(
    year: int = typer.Argument(..., help="Publication year to filter by"),
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")     
):
    """Sync bibliography for a specific publication year"""
    print("[cyan]Fetching bibliography...[/cyan]")
    provider = ZoteroProvider(group_id=groupid, collection=collection)
    raw_items = provider.fetch()
    print(f"[green]Fetched {len(raw_items)} items[/green]")
    filtered = [i for i in raw_items if str(year) in (i.get("data", {}).get("date") or "")]
    print(f"[yellow]Filtered down to {len(filtered)} items for year {year}[/yellow]")
    _run_sync(filtered, output, suffix=f"_{year}")