"""Bitwig CLI - Workflow commands for Bitwig Studio.

For direct control commands (device params, RPC calls), use `groove-link` instead.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import yaml

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

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
from .devices import search_devices
from .kontakt import search_kontakt
from .mtron import search_mtron
from .plugins import search_plugins
from .presets import search_presets
from .resolve import resolve_device
from .table import Column, adaptive_table

# CLI app
app = typer.Typer(
    name="bitwig",
    help="Workflow commands for Bitwig Studio. For direct control, use `groove-link`.",
    no_args_is_help=True,
)

# Rich console for formatted output
console = Console()


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


@app.command()
def device(
    query: Annotated[str, typer.Argument(help="Search query (fuzzy, case insensitive)")],
    limit: Annotated[int, typer.Option("-n", "--limit", help="Max results")] = 20,
    category: Annotated[
        str | None,
        typer.Option("-c", "--category", help="Filter by category: inst, note, fx, routing, mod, util"),
    ] = None,
    paths: Annotated[bool, typer.Option("--paths", help="Output file paths only")] = False,
    verbose: VerboseOption = False,
) -> None:
    """Search for Bitwig base devices.

    Base devices are the core Bitwig devices like Audio Receiver, Compressor,
    Polymer, etc. (not presets or plugins).

    Examples:
        bitwig device receiver
        bitwig device "audio receiver"
        bitwig device compressor -c fx
        bitwig device polymer --category inst
        bitwig device note -c note
    """
    import time

    setup_logging(verbose)
    start = time.perf_counter()

    # Validate category filter
    valid_categories = {"inst", "note", "fx", "routing", "mod", "util"}
    if category and category not in valid_categories:
        rprint(f"[red]Error:[/red] Invalid category '{category}'")
        rprint(f"[dim]Valid categories: {', '.join(sorted(valid_categories))}[/dim]")
        raise typer.Exit(1)

    results = search_devices(query, limit=limit, category_filter=category)
    elapsed = time.perf_counter() - start

    if not results:
        rprint(f"[yellow]No devices found for '{query}'[/yellow]")
        raise typer.Exit(0)

    if paths:
        for r in results:
            print(r.file_path)
    else:
        columns = [
            Column("Name", "name", min_width=15, max_width=30, priority=3),
            Column("Load", "load_type", min_width=6, max_width=6, priority=3),
            Column("Category", "category", min_width=7, max_width=10, priority=2),
        ]
        table = adaptive_table(results, columns)
        wide_console = Console(width=300)
        wide_console.print(table)
        rprint(f"[dim]Found {len(results)} devices in {elapsed:.2f}s[/dim]")


# Project subcommand group
project_app = typer.Typer(help="Project setup from song config")
app.add_typer(project_app, name="project")


@project_app.command("create")
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
    """Create tracks with devices from a declarative song config.

    Example config:

        song:
          title: Morning Light
          tempo: 88
          key: G

        groups:
          rhythm:
            tracks: [piano, bass]

        tracks:
          piano:
            instrument: nektar piano
            note_fx:
              - Humanize x 3
            fx:
              - Tape-Machine
              - Room One
            part: piano.abc

          bass:
            instrument: Acoustic Bass Long
            fx:
              - Warm Saturator
              - Room One
            part: bass.abc

    Track fields:
      - instrument: main sound source (required for instrument tracks)
      - note_fx: note-level effects (before instrument)
      - fx: audio effects (after instrument)
      - part: ABC or MIDI file for clip launcher

    Use --track to create a specific track, or omit to create all.
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

    # Parse declarative format: song metadata at top level or in 'song' section
    song_meta = config.get("song", {})
    song_title = song_meta.get("title") or config.get("name", "Untitled")

    # Get tracks section
    tracks_config = config.get("tracks", {})
    if not tracks_config:
        rprint("[red]Error:[/red] No tracks defined in config")
        raise typer.Exit(1)

    # Get groups (for future use - API may not support programmatic grouping)
    groups_config = config.get("groups", {})
    if groups_config:
        rprint(f"[dim]Groups defined: {', '.join(groups_config.keys())}[/dim]")

    rprint(f"[cyan]Song:[/cyan] {song_title}")

    # Set tempo from song.tempo or legacy bpm field
    tempo = song_meta.get("tempo") or config.get("bpm") or config.get("tempo")
    if tempo:
        _set_tempo(tempo, host, port)

    # Filter to specific track if requested
    if track_name:
        if track_name not in tracks_config:
            rprint(f"[red]Error:[/red] Track '{track_name}' not found in config")
            rprint(f"[dim]Available tracks: {', '.join(tracks_config.keys())}[/dim]")
            raise typer.Exit(1)
        tracks_config = {track_name: tracks_config[track_name]}

    # Get config directory for resolving relative MIDI paths
    config_dir = config_file.parent

    # Get all track names for cross-referencing (e.g., receives)
    all_track_names = list(tracks_config.keys())

    # Create each track
    created_count = 0
    midi_inserted = 0
    for track_index, (tname, track_cfg) in enumerate(tracks_config.items()):
        if not _create_track(tname, track_cfg, host, port, all_track_names):
            rprint(f"[red]Failed to create track:[/red] {tname}")
            continue

        created_count += 1

        # Get part file (declarative) or legacy abc/midi fields
        part_file = track_cfg.get("part")
        abc_file = track_cfg.get("abc") if not part_file else None
        midi_file = track_cfg.get("midi") if not part_file else None

        # Determine if part is ABC or MIDI based on extension
        if part_file:
            if part_file.endswith(".abc"):
                abc_file = part_file
            elif part_file.endswith(".mid") or part_file.endswith(".midi"):
                midi_file = part_file
            else:
                # Default to ABC
                abc_file = part_file

        if abc_file:
            from .abc import abc_to_midi

            abc_path = Path(abc_file)
            if not abc_path.is_absolute():
                abc_path = config_dir / abc_path
            abc_path = abc_path.resolve()

            if not abc_path.exists():
                rprint(f"  [yellow]Warning:[/yellow] ABC file not found: {abc_path}")
            else:
                rprint(f"  [dim]Converting ABC:[/dim] {abc_path.name}")
                result = abc_to_midi(abc_path)
                if result.success and result.midi_file:
                    midi_file = str(result.midi_file)
                    rprint(f"  [green]✓[/green] Converted to {result.midi_file.name}")
                    if result.warnings:
                        for warn in result.warnings[:3]:
                            rprint(f"    [dim]{warn}[/dim]")
                else:
                    rprint(f"  [red]✗[/red] ABC conversion failed: {result.error}")

        # Insert MIDI if specified (or converted from ABC)
        if midi_file:
            midi_path = Path(midi_file)
            if not midi_path.is_absolute():
                midi_path = config_dir / midi_path
            midi_path = midi_path.resolve()

            if not midi_path.exists():
                rprint(f"  [yellow]Warning:[/yellow] MIDI file not found: {midi_path}")
            else:
                rprint(f"  [dim]Inserting MIDI:[/dim] {midi_path.name}")
                if _insert_midi(track_index, 0, str(midi_path), host, port):
                    rprint(f"  [green]✓[/green] MIDI inserted into slot 1")
                    midi_inserted += 1
                else:
                    rprint(f"  [red]✗[/red] Failed to insert MIDI")

    elapsed = time.perf_counter() - start
    summary = f"Created {created_count}/{len(tracks_config)} tracks"
    if midi_inserted > 0:
        summary += f", inserted {midi_inserted} MIDI files"
    rprint(f"[green]✓[/green] {summary} in {elapsed:.2f}s")


def _create_track(
    name: str,
    track_cfg: dict,
    host: str,
    port: int,
    all_track_names: list[str] | None = None,
) -> bool:
    """Create a single track with devices.

    Supports declarative format:
        instrument: nektar piano
        note_fx: [Humanize x 3]
        fx: [Tape-Machine, Room One]

    Or receives format (for shared FX):
        receives:
          - piano: pre
          - bass: pre
        fx: [Reverb, Delay]

    Or master track (adds to master bus, no new track):
        master:
          fx: [EQ-5, Peak Limiter]

    Or legacy format:
        devices: [Humanize x 3, nektar piano, Tape-Machine]

    Returns True on success, False on failure.
    """
    # Special case: master track adds devices to master bus
    is_master = name.lower() == "master"

    # Determine track type from config
    track_type = track_cfg.get("type", "instrument")
    if is_master:
        track_type = "master"  # Signal to extension: add to master bus
    elif "instrument" in track_cfg:
        track_type = "instrument"
    elif "receives" in track_cfg:
        track_type = "audio"  # Receiving tracks are audio tracks

    # Build device list from declarative format
    device_specs = []
    audio_receiver_sources = []  # Track names to receive from

    # Handle receives: add Audio Receiver for each source
    receives = track_cfg.get("receives", [])
    if receives:
        for recv_spec in receives:
            # recv_spec is either "track_name" or {"track_name": "pre/post"}
            if isinstance(recv_spec, str):
                source_track = recv_spec
                tap = "pre"
            elif isinstance(recv_spec, dict):
                # {"piano": "pre"} format
                source_track = list(recv_spec.keys())[0]
                tap = recv_spec[source_track]
            else:
                rprint(f"[yellow]Warning:[/yellow] Invalid receives spec: {recv_spec}")
                continue

            audio_receiver_sources.append((source_track, tap))
            # Add Audio Receiver device (will need source param set later)
            device_specs.append({"query": "Audio Receiver", "hint": "device"})

    # Handle declarative instrument/note_fx/fx format
    if "instrument" in track_cfg or "note_fx" in track_cfg or "fx" in track_cfg:
        device_specs.extend(track_cfg.get("note_fx", []))
        if "instrument" in track_cfg:
            device_specs.append(track_cfg["instrument"])
        device_specs.extend(track_cfg.get("fx", []))
    elif not receives:
        # Legacy format: flat devices list
        device_specs = track_cfg.get("devices", [])

    # Resolve device names to actual paths
    if is_master:
        rprint(f"[cyan]Master bus:[/cyan] adding {len(device_specs)} devices")
    else:
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
        devices_loaded = rpc_result.get("devicesAdded", 0)
        if is_master:
            rprint(f"  [green]✓[/green] Added {devices_loaded} devices to master bus")
        else:
            rprint(f"  [green]✓[/green] Created with {devices_loaded} devices")

    # Note about Audio Receiver sources (parameter setting is TODO)
    if audio_receiver_sources:
        for source_track, tap in audio_receiver_sources:
            rprint(f"  [dim]Audio Receiver:[/dim] source={source_track} ({tap})")
        rprint(f"  [yellow]Note:[/yellow] Audio Receiver sources need manual configuration")

    return True


def _set_tempo(bpm: float, host: str, port: int) -> bool:
    """Set the project tempo.

    Returns True on success, False on failure.
    """
    rprint(f"[cyan]Setting tempo:[/cyan] {bpm} BPM")

    with get_client(host, port) as client:
        try:
            result = client.call("transport.setTempo", {"bpm": float(bpm)})
            rprint(f"[green]✓[/green] Tempo set to {result.get('bpm', bpm)} BPM")
            return True
        except RPCException as e:
            rprint(f"[red]Error setting tempo:[/red] {e}")
            return False


def _insert_midi(
    track_index: int,
    slot_index: int,
    midi_path: str,
    host: str,
    port: int,
) -> bool:
    """Insert a MIDI file into a clip launcher slot.

    Args:
        track_index: Track index (0-based)
        slot_index: Clip launcher slot index (0-based)
        midi_path: Absolute path to MIDI file
        host: Controller host
        port: Controller port

    Returns True on success, False on failure.
    """
    with get_client(host, port) as client:
        try:
            client.call(
                "clip.insertFile",
                {
                    "trackIndex": track_index,
                    "slotIndex": slot_index,
                    "path": midi_path,
                },
            )
            return True
        except RPCException as e:
            rprint(f"[red]Error inserting MIDI:[/red] {e}")
            return False


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"bitwig {__version__}")


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-V", help="Show version and exit", is_eager=True),
    ] = None,
) -> None:
    """Workflow commands for Bitwig Studio.

    For direct control (device params, RPC calls), use `groove-link` instead.
    """
    if version:
        rprint(f"bitwig {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
