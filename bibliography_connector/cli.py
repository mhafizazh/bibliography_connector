import typer
import yaml

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
def sync(config_path: str = "config.yaml"):

    with open(config_path) as f:
        config = yaml.safe_load(f)

    print("[cyan]Fetching bibliography...[/cyan]")

    provider = ZoteroProvider(
        group_id=config["source"]["group_id"],
        collection=config["source"]["collection"]
    )

    raw_items = provider.fetch()

    print(f"[green]Fetched {len(raw_items)} items[/green]")

    items = run_pipeline(raw_items)

    print(f"[yellow]Processed {len(items)} items[/yellow]")

    exporter = HugoExporter(
        output_dir=config["output"]["markdown_dir"],
        json_file=config["output"]["json_file"]
    )

    exporter.export(items)

    print("[bold green]Export complete[/bold green]")

if __name__ == "__main__":
    app()