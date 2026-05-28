import typer
from .cmd_sync import sync_app
app = typer.Typer(help="Bibliography connector CLI")
app.add_typer(sync_app, name="sync")