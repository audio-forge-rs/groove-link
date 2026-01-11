"""Bitwig CLI - Main entry point."""

from __future__ import annotations

import logging
import sys
from typing import Annotated, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from . import __version__
from .client import BitwigClient, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TIMEOUT
from .protocol import RPCException

# CLI app
app = typer.Typer(
    name="bitwig",
    help="Control Bitwig Studio from the command line.",
    no_args_is_help=True,
)

# Rich console for formatted output
console = Console()

# Common options
HostOption = Annotated[
    str,
    typer.Option("--host", "-h", help="Bitwig controller host", envvar="BITWIG_HOST"),
]
PortOption = Annotated[
    int,
    typer.Option("--port", "-p", help="Bitwig controller RPC port", envvar="BITWIG_RPC_PORT"),
]
VerboseOption = Annotated[
    bool,
    typer.Option("--verbose", "-v", help="Enable verbose output"),
]


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def get_client(host: str, port: int) -> BitwigClient:
    """Create and connect a client, handling connection errors."""
    client = BitwigClient(host=host, port=port)
    try:
        client.connect()
    except ConnectionRefusedError:
        rprint(f"[red]Error:[/red] Cannot connect to Bitwig controller at {host}:{port}")
        rprint("[dim]Is Bitwig Studio running with the controller extension enabled?[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        rprint(f"[red]Error:[/red] Connection failed: {e}")
        raise typer.Exit(1)
    return client


@app.command()
def info(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Show Bitwig and controller information."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            result = client.call("info.get")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    # Display info in a nice table
    table = Table(title="Bitwig Controller Info", show_header=False)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("CLI Version", __version__)
    table.add_row("Controller Version", result.get("controllerVersion", "unknown"))
    table.add_row("Bitwig Version", result.get("bitwigVersion", "unknown"))
    table.add_row("API Version", str(result.get("apiVersion", "unknown")))
    table.add_row("Project", result.get("projectName", "(no project)"))
    table.add_row("Platform", result.get("platform", "unknown"))

    console.print(table)


@app.command("list")
def list_cmd(
    what: Annotated[
        str,
        typer.Argument(help="What to list: tracks, devices, scenes, clips"),
    ],
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """List tracks, devices, scenes, or clips."""
    setup_logging(verbose)

    method_map = {
        "tracks": "list.tracks",
        "devices": "list.devices",
        "scenes": "list.scenes",
        "clips": "list.clips",
    }

    if what not in method_map:
        rprint(f"[red]Error:[/red] Unknown list type: {what}")
        rprint(f"[dim]Valid options: {', '.join(method_map.keys())}[/dim]")
        raise typer.Exit(1)

    with get_client(host, port) as client:
        try:
            result = client.call(method_map[what])
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    # For now, just print the result - we'll format better once we know the structure
    rprint(result)


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"bitwig-cli {__version__}")


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-V", help="Show version and exit", is_eager=True),
    ] = None,
) -> None:
    """Control Bitwig Studio from the command line."""
    if version:
        rprint(f"bitwig-cli {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
