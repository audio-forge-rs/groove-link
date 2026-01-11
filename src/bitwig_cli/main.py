"""Bitwig CLI - Main entry point."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Annotated, Optional

import yaml

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from . import __version__
from .client import BitwigClient, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TIMEOUT
from .kontakt import search_kontakt
from .mtron import search_mtron
from .plugins import search_plugins
from .presets import search_presets
from .protocol import RPCException
from .resolve import resolve_device
from .table import Column, adaptive_table

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
def preset(
    query: Annotated[str, typer.Argument(help="Search query (fuzzy, case insensitive)")],
    limit: Annotated[int, typer.Option("-n", "--limit", help="Max results")] = 20,
    type_filter: Annotated[
        str | None,
        typer.Option("-t", "--type", help="Filter by type: inst, note, or fx"),
    ] = None,
    paths: Annotated[bool, typer.Option("--paths", help="Output file paths only")] = False,
    verbose: VerboseOption = False,
) -> None:
    """Search for Bitwig presets by name.

    Examples:
        bitwig preset nektar
        bitwig preset "warm pad"
        bitwig preset bass -n 10
        bitwig preset delay --type fx
        bitwig preset arp -t note
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    # Get more results if filtering, then filter down
    fetch_limit = limit * 5 if type_filter else limit
    results = search_presets(query, limit=fetch_limit)

    # Filter by type if specified
    if type_filter:
        type_filter = type_filter.lower()
        if type_filter not in ("inst", "note", "fx"):
            rprint(f"[red]Error:[/red] Invalid type '{type_filter}'. Use: inst, note, or fx")
            raise typer.Exit(1)
        results = [r for r in results if r.device_type == type_filter][:limit]
    elapsed = time.perf_counter() - start

    if not results:
        rprint(f"[yellow]No presets found for '{query}'[/yellow]")
        raise typer.Exit(0)

    if paths:
        for r in results:
            print(r.file_path)
    else:
        columns = [
            Column("Name", "name", min_width=15, max_width=28, priority=3),
            Column("Load", "load_type", min_width=4, max_width=6, priority=3),
            Column("Type", "device_type", min_width=4, max_width=4, priority=2),
            Column("Device", "device", min_width=8, max_width=12, priority=2),
            Column("Pack", "pack", min_width=10, max_width=24, priority=1),
            Column("Package", "package", min_width=6, max_width=12, priority=1),
        ]
        table = adaptive_table(results, columns)
        # Use wide console to prevent truncation - allows horizontal scroll
        wide_console = Console(width=300)
        wide_console.print(table)
        rprint(f"[dim]Found {len(results)} presets in {elapsed:.2f}s[/dim]")


@app.command()
def plugin(
    query: Annotated[str, typer.Argument(help="Search query (fuzzy, case insensitive)")],
    limit: Annotated[int, typer.Option("-n", "--limit", help="Max results")] = 20,
    format_filter: Annotated[
        str | None,
        typer.Option("-f", "--format", help="Filter by format: vst3, au, clap"),
    ] = None,
    paths: Annotated[bool, typer.Option("--paths", help="Output file paths only")] = False,
    verbose: VerboseOption = False,
) -> None:
    """Search for audio plugins (VST3, AU, CLAP).

    Examples:
        bitwig plugin kontakt
        bitwig plugin "native instruments"
        bitwig plugin surge --format clap
        bitwig plugin compressor -n 10
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    results = search_plugins(query, limit=limit, format_filter=format_filter)
    elapsed = time.perf_counter() - start

    if not results:
        rprint(f"[yellow]No plugins found for '{query}'[/yellow]")
        raise typer.Exit(0)

    if paths:
        for r in results:
            print(r.file_path)
    else:
        columns = [
            Column("Name", "name", min_width=15, max_width=30, priority=3),
            Column("Load", "load_type", min_width=4, max_width=5, priority=3),
            Column("Vendor", "vendor", min_width=10, max_width=20, priority=2),
            Column("Version", "version", min_width=5, max_width=10, priority=1),
            Column("Location", "location", min_width=4, max_width=6, priority=1),
        ]
        table = adaptive_table(results, columns)
        wide_console = Console(width=300)
        wide_console.print(table)
        rprint(f"[dim]Found {len(results)} plugins in {elapsed:.2f}s[/dim]")


@app.command()
def kontakt(
    query: Annotated[str, typer.Argument(help="Search query (fuzzy, case insensitive)")],
    limit: Annotated[int, typer.Option("-n", "--limit", help="Max results")] = 20,
    library: Annotated[
        str | None,
        typer.Option("-l", "--library", help="Filter by library name"),
    ] = None,
    paths: Annotated[bool, typer.Option("--paths", help="Output file paths only")] = False,
    verbose: VerboseOption = False,
) -> None:
    """Search for Kontakt instruments.

    Examples:
        bitwig kontakt piano
        bitwig kontakt "electric sunburst"
        bitwig kontakt bass --library "Session Guitarist"
        bitwig kontakt strings -n 10
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    results = search_kontakt(query, limit=limit, library_filter=library)
    elapsed = time.perf_counter() - start

    if not results:
        rprint(f"[yellow]No Kontakt instruments found for '{query}'[/yellow]")
        raise typer.Exit(0)

    if paths:
        for r in results:
            print(r.file_path)
    else:
        columns = [
            Column("Name", "name", min_width=15, max_width=35, priority=3),
            Column("Load", "load_type", min_width=7, max_width=7, priority=3),
            Column("Library", "library", min_width=15, max_width=40, priority=2),
            Column("Vendor", "vendor", min_width=10, max_width=20, priority=1),
        ]
        table = adaptive_table(results, columns)
        wide_console = Console(width=300)
        wide_console.print(table)
        rprint(f"[dim]Found {len(results)} instruments in {elapsed:.2f}s[/dim]")


@app.command()
def mtron(
    query: Annotated[str, typer.Argument(help="Search query (fuzzy, case insensitive)")],
    limit: Annotated[int, typer.Option("-n", "--limit", help="Max results")] = 20,
    collection: Annotated[
        str | None,
        typer.Option("-c", "--collection", help="Filter by collection/tape bank"),
    ] = None,
    category: Annotated[
        str | None,
        typer.Option("--category", help="Filter by category (Strings, Brass, etc.)"),
    ] = None,
    paths: Annotated[bool, typer.Option("--paths", help="Output file paths only")] = False,
    verbose: VerboseOption = False,
) -> None:
    """Search for M-Tron Pro IV patches.

    Examples:
        bitwig mtron violins
        bitwig mtron flute --category Woodwind
        bitwig mtron choir -c "Streetly Tapes"
        bitwig mtron strings -n 10
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    results = search_mtron(
        query, limit=limit, collection_filter=collection, category_filter=category
    )
    elapsed = time.perf_counter() - start

    if not results:
        rprint(f"[yellow]No M-Tron patches found for '{query}'[/yellow]")
        raise typer.Exit(0)

    if paths:
        for r in results:
            print(r.file_path)
    else:
        columns = [
            Column("Name", "name", min_width=15, max_width=35, priority=3),
            Column("Load", "load_type", min_width=5, max_width=5, priority=3),
            Column("Collection", "collection", min_width=15, max_width=35, priority=2),
            Column("Category", "category", min_width=8, max_width=15, priority=2),
        ]
        table = adaptive_table(results, columns)
        wide_console = Console(width=300)
        wide_console.print(table)
        rprint(f"[dim]Found {len(results)} patches in {elapsed:.2f}s[/dim]")


# Track subcommand group
track_app = typer.Typer(help="Track operations")
app.add_typer(track_app, name="track")


@track_app.command("create")
def track_create(
    config_file: Annotated[
        Path,
        typer.Argument(help="YAML config file (song config with tracks section)"),
    ],
    track_name: Annotated[
        Optional[str],
        typer.Option("--track", "-t", help="Specific track to create (default: all)"),
    ] = None,
    host: HostOption = DEFAULT_HOST,
    port: PortOption = DEFAULT_PORT,
    verbose: VerboseOption = False,
) -> None:
    """Create tracks with devices from a song YAML config.

    The YAML config file can define tracks in a 'tracks' section:

        name: My Song
        bpm: 120

        tracks:
          piano:
            type: instrument
            devices:
              - Humanize
              - nektar piano
              - query: abbey road
                hint: plugin

          bass:
            type: instrument
            devices:
              - bass preset

    Use --track to create a specific track, or omit to create all tracks.

    Device entries can be:
      - A string (fuzzy searched as preset then plugin)
      - A dict with 'query' and optional 'hint' (preset/plugin/kontakt/mtron)
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    # Load and parse YAML config
    if not config_file.exists():
        rprint(f"[red]Error:[/red] Config file not found: {config_file}")
        raise typer.Exit(1)

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        rprint(f"[red]Error:[/red] Invalid YAML: {e}")
        raise typer.Exit(1)

    if not isinstance(config, dict):
        rprint("[red]Error:[/red] Config must be a YAML mapping")
        raise typer.Exit(1)

    # Get tracks section (or use whole config if no tracks section)
    tracks_config = config.get("tracks", {})
    if not tracks_config:
        # Backwards compat: if no 'tracks' section, treat whole config as single track
        single_name = config.get("name", "New Track")
        tracks_config = {single_name: config}

    # Filter to specific track if requested
    if track_name:
        if track_name not in tracks_config:
            rprint(f"[red]Error:[/red] Track '{track_name}' not found in config")
            rprint(f"[dim]Available tracks: {', '.join(tracks_config.keys())}[/dim]")
            raise typer.Exit(1)
        tracks_config = {track_name: tracks_config[track_name]}

    # Create each track
    created_count = 0
    for tname, track_cfg in tracks_config.items():
        if not _create_track(tname, track_cfg, host, port):
            rprint(f"[red]Failed to create track:[/red] {tname}")
        else:
            created_count += 1

    elapsed = time.perf_counter() - start
    rprint(f"[green]✓[/green] Created {created_count}/{len(tracks_config)} tracks in {elapsed:.2f}s")


def _create_track(
    name: str,
    track_cfg: dict,
    host: str,
    port: int,
) -> bool:
    """Create a single track with devices.

    Returns True on success, False on failure.
    """
    track_type = track_cfg.get("type", "instrument")
    device_specs = track_cfg.get("devices", [])

    # Resolve device names to actual paths
    rprint(f"[cyan]Creating track:[/cyan] {name} ({track_type})")
    resolved_devices = []
    for spec in device_specs:
        if isinstance(spec, str):
            # Simple string query
            query = spec
            hint = None
        elif isinstance(spec, dict):
            query = spec.get("query", spec.get("name", ""))
            hint = spec.get("hint")
        else:
            rprint(f"[yellow]Warning:[/yellow] Skipping invalid device spec: {spec}")
            continue

        rprint(f"  [dim]Resolving:[/dim] {query}...", end="")
        result = resolve_device(query, hint)

        if result.success and result.spec:
            resolved_devices.append(result.spec.to_dict())
            rprint(f" [green]→[/green] {result.spec.display_name} ({result.spec.type})")
        else:
            rprint(f" [red]✗[/red] {result.error}")
            if result.alternatives:
                rprint(f"    [dim]Suggestions: {', '.join(result.alternatives)}[/dim]")

    if not resolved_devices and not device_specs:
        rprint("  [dim]No devices specified[/dim]")

    # Build RPC params
    params = {
        "name": name,
        "type": track_type,
        "devices": resolved_devices,
    }

    # Progress callback
    def on_progress(step: int, total: int, message: str) -> None:
        rprint(f"  [dim][{step}/{total}][/dim] {message}")

    # Make RPC call with progress
    with get_client(host, port) as client:
        try:
            # Longer timeout for track creation with multiple devices
            timeout = 5.0 + len(resolved_devices) * 2.0
            rpc_result = client.call_with_progress(
                "track.create",
                params,
                on_progress=on_progress,
                timeout=timeout,
            )
        except RPCException as e:
            rprint(f"  [red]Error:[/red] {e}")
            return False

    # Show result details
    if isinstance(rpc_result, dict):
        devices_loaded = rpc_result.get("devices", 0)
        rprint(f"  [green]✓[/green] Created with {devices_loaded} devices")

    return True


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
