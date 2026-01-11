"""Groove Link CLI - Internal tool for direct Bitwig control.

This is an INTERNAL tool for debugging, testing, and fine-grained manipulation.
Not intended for end users - use the `bitwig` CLI for workflow commands.

Commands:
  groove-link device list-params     List parameter IDs for current device
  groove-link device select-first    Select first device in chain
  groove-link device select-next     Select next device in chain
  groove-link device select-last     Select last device in chain
  groove-link device set-param ID V  Set a device parameter
  groove-link call METHOD [PARAMS]   Call any RPC method directly
  groove-link status                 Check connection status
"""

from __future__ import annotations

from typing import Annotated

import typer
from rich import print as rprint

from . import __version__
from .common import (
    HostOption,
    PortOption,
    VerboseOption,
    setup_logging,
    get_client,
    DEFAULT_HOST,
    DEFAULT_PORT,
    RPCException,
)

# CLI app
app = typer.Typer(
    name="groove-link",
    help="Direct control commands for Bitwig Studio. For workflow commands, use `bitwig`.",
    no_args_is_help=True,
)


# ==================== Device Commands ====================

device_app = typer.Typer(help="Device selection and parameter control")
app.add_typer(device_app, name="device")


@device_app.command("list-params")
def device_list_params(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """List parameter IDs for the currently selected device."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            result = client.call("device.listParams")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    if not result:
        rprint("[yellow]No parameters found (is a device selected?)[/yellow]")
        raise typer.Exit(0)

    rprint(f"[cyan]Device parameters ({len(result)}):[/cyan]")
    for param_id in result:
        rprint(f"  {param_id}")


@device_app.command("select-first")
def device_select_first(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Select the first device in the track's device chain."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            result = client.call("device.selectFirst")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    device = result.get("device", "")
    exists = result.get("exists", False)
    if exists:
        rprint(f"[green]✓[/green] Selected: {device}")
    else:
        rprint("[yellow]No device found[/yellow]")


@device_app.command("select-next")
def device_select_next(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Select the next device in the track's device chain."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            result = client.call("device.selectNext")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    device = result.get("device", "")
    exists = result.get("exists", False)
    if exists:
        rprint(f"[green]✓[/green] Selected: {device}")
    else:
        rprint("[yellow]End of device chain[/yellow]")


@device_app.command("select-last")
def device_select_last(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Select the last device in the track's device chain."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            client.call("device.selectLast")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    rprint("[green]✓[/green] Selected last device")


@device_app.command("set-param")
def device_set_param(
    param_id: Annotated[str, typer.Argument(help="Parameter ID (from list-params)")],
    value: Annotated[float, typer.Argument(help="Normalized value (0.0 to 1.0)")],
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Set a device parameter by ID.

    Example:
        groove-link device set-param "CONTENTS/MIX" 0.5
    """
    setup_logging(verbose)

    if value < 0.0 or value > 1.0:
        rprint("[red]Error:[/red] Value must be between 0.0 and 1.0")
        raise typer.Exit(1)

    with get_client(host, port) as client:
        try:
            result = client.call("device.setParameter", {
                "parameterId": param_id,
                "value": value,
            })
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    rprint(f"[green]✓[/green] Set {result.get('parameterId', param_id)} = {result.get('value', value)}")


# ==================== RPC Commands ====================

@app.command("call")
def rpc_call(
    method: Annotated[str, typer.Argument(help="RPC method name")],
    params: Annotated[str, typer.Argument(help="JSON params")] = "{}",
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Call any RPC method directly.

    Example:
        groove-link call info.get
        groove-link call device.setParameter '{"parameterId": "MIX", "value": 0.5}'
    """
    import json

    setup_logging(verbose)

    try:
        params_dict = json.loads(params)
    except json.JSONDecodeError as e:
        rprint(f"[red]Error:[/red] Invalid JSON params: {e}")
        raise typer.Exit(1)

    with get_client(host, port) as client:
        try:
            result = client.call(method, params_dict)
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    # Pretty print result
    if isinstance(result, (dict, list)):
        rprint(json.dumps(result, indent=2))
    else:
        rprint(result)


# ==================== Status Commands ====================

@app.command()
def status(
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Check connection status and versions."""
    setup_logging(verbose)

    with get_client(host, port) as client:
        try:
            result = client.call("info.get")
        except RPCException as e:
            rprint(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    rprint("[green]Connected[/green]")
    rprint(f"  Controller: v{result.get('controllerVersion', '?')}")
    rprint(f"  Bitwig: v{result.get('bitwigVersion', '?')}")
    rprint(f"  Project: {result.get('projectName', '(none)')}")


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"groove-link {__version__}")


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", "-V", help="Show version and exit", is_eager=True),
    ] = None,
) -> None:
    """Direct control commands for Bitwig Studio."""
    if version:
        rprint(f"groove-link {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
