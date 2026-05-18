import typer
import os
from rich import print

from bibliography_connector.providers.zotero import ZoteroProvider
from bibliography_connector.pipeline import run_pipeline
from bibliography_connector.exporters.hugo import HugoExporter

app = typer.Typer()

@app.callback()
def main():
    """Bibliography connector CLI"""
    pass

@app.command("sync")
def sync(
    groupid: str = typer.Option(..., "--groupid", "-g", help="zotero group id value"),
    collection: str = typer.Option(..., "--collectionid", "-c", help="zotero collection id value"),
    output: str = typer.Option(..., "--outdir", "-o", help="output path destination")     
):

    print("[cyan]Fetching bibliography...[/cyan]")

    provider = ZoteroProvider(
        group_id=groupid,
        collection=collection
    )

    raw_items = provider.fetch()

    print(f"[green]Fetched {len(raw_items)} items[/green]")

    items = run_pipeline(raw_items)

    print(f"[yellow]Processed {len(items)} items[/yellow]")

    exporter = HugoExporter(
        output_dir=output,
        json_file=os.path.join(output, "bibliography.json")
    )

    exporter.export(items)

    print("[bold green]Export complete[/bold green]")

if __name__ == "__main__":
    app()