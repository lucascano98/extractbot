import sys
import typer
from typing import Annotated
from importlib.metadata import version
from rich.console import Console
from rich.table import Table
from enum import StrEnum, auto

__version__ = version('extractbot')

console = Console()
err_console = Console(stderr=True, style="bold red")
app = typer.Typer()

def version_callback(value: bool):
    if value:
        console.print(f"[green]Extractbot Version: {__version__}[/green]")
        raise typer.Exit()


class Format(StrEnum):
    TABLE = auto()
    JSON = auto()
    MARKDOWN = auto()

@app.callback()
def main(
        version: Annotated[bool | None, typer.Option("--version", callback=version_callback, help="Show the version and exit.")] = None):
    pass

@app.command()
def parse(path: Annotated[str, typer.Argument()],
          format: Annotated[Format, typer.Option("--format", help="Format the text as a table, json, or markdown.")] = Format.TABLE):
    try:
        if path == "-":
            data = sys.stdin.read()
        else:
            with open(path, 'r') as file:
                data = file.read()
    
    except FileNotFoundError as e:
        err_console.print(f"Error: {e}")
        raise typer.Exit(code=1)
    except PermissionError as e:
        err_console.print(f"Error: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        err_console.print(f"Error: {e}")
        raise typer.Exit(code=1)

    if not data.strip():
        err_console.print(f"Input is empty")
        raise typer.Exit(code=1)

    console.print(data)
