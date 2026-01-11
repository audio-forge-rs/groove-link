"""Common utilities shared between bitwig and groove-link CLIs."""

from __future__ import annotations

import logging
from typing import Annotated

import typer
from rich import print as rprint

from .client import BitwigClient, DEFAULT_HOST, DEFAULT_PORT
from .protocol import RPCException

# Common CLI options - reusable type annotations
HostOption = Annotated[
    str,
    typer.Option("--host", "-h", help="Server host", envvar="BITWIG_HOST"),
]
PortOption = Annotated[
    int,
    typer.Option("--port", "-p", help="Server port", envvar="BITWIG_RPC_PORT"),
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
        rprint(f"[red]Error:[/red] Cannot connect to server at {host}:{port}")
        rprint("[dim]Is the groove-link server running?[/dim]")
        raise typer.Exit(1)
    except Exception as e:
        rprint(f"[red]Error:[/red] Connection failed: {e}")
        raise typer.Exit(1)
    return client


__all__ = [
    "HostOption",
    "PortOption",
    "VerboseOption",
    "setup_logging",
    "get_client",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "RPCException",
]
