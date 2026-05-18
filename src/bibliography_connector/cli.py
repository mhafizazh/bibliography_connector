import click
from bibliography_connector.commands.get_item import get_item


@click.group()
def app():
    """bibconnectorCLI python library to connect zotero to json"""
    pass
app.add_command(get_item)
if __name__ == "__main__":
    app()