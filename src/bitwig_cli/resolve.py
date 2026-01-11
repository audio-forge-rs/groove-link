"""Device resolution: resolve fuzzy names to actual device specs.

This module takes user-friendly names like "nektar piano" or "abbey road"
and resolves them to actual device specifications that Bitwig can load.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .kontakt import search_kontakt
from .mtron import search_mtron
from .plugins import search_plugins
from .presets import search_presets


@dataclass
class DeviceSpec:
    """Resolved device specification for Bitwig insertion."""

    type: Literal["file", "vst3", "clap", "vst2"]
    path: str  # File path or plugin ID
    display_name: str  # Human-readable name for progress display

    def to_dict(self) -> dict:
        return {"type": self.type, "path": self.path}


@dataclass
class ResolveResult:
    """Result of resolving a device name."""

    success: bool
    spec: DeviceSpec | None
    error: str | None = None
    alternatives: list[str] | None = None  # Suggestions if not found


def resolve_preset(query: str, device_type: str | None = None) -> ResolveResult:
    """Resolve a preset name to a file path.

    Args:
        query: Fuzzy search query (e.g., "nektar piano", "warm pad")
        device_type: Optional filter: "inst", "note", or "fx"

    Returns:
        ResolveResult with the resolved DeviceSpec or error
    """
    results = search_presets(query, limit=5)

    if device_type:
        results = [r for r in results if r.device_type == device_type]

    if not results:
        return ResolveResult(
            success=False,
            spec=None,
            error=f"No preset found for '{query}'",
        )

    # Take the best match
    best = results[0]
    spec = DeviceSpec(
        type="file",
        path=best.file_path,
        display_name=best.name,
    )

    # Include alternatives for feedback
    alternatives = [r.name for r in results[1:4]] if len(results) > 1 else None

    return ResolveResult(success=True, spec=spec, alternatives=alternatives)


def resolve_plugin(query: str, format_filter: str | None = None) -> ResolveResult:
    """Resolve a plugin name to a path and format.

    Args:
        query: Fuzzy search query (e.g., "abbey road", "kontakt")
        format_filter: Optional filter: "vst3", "au", "clap", "vst"

    Returns:
        ResolveResult with the resolved DeviceSpec or error
    """
    results = search_plugins(query, limit=5, format_filter=format_filter)

    if not results:
        return ResolveResult(
            success=False,
            spec=None,
            error=f"No plugin found for '{query}'",
        )

    # Take the best match
    best = results[0]

    # Map format to device load type
    load_type: Literal["file", "vst3", "clap", "vst2"]
    if best.format == "clap":
        load_type = "clap"
    elif best.format == "vst":
        load_type = "vst2"
    else:
        load_type = "vst3"  # vst3 and au both use vst3 API

    spec = DeviceSpec(
        type=load_type,
        path=best.file_path,
        display_name=best.name,
    )

    alternatives = [r.name for r in results[1:4]] if len(results) > 1 else None

    return ResolveResult(success=True, spec=spec, alternatives=alternatives)


def resolve_kontakt(query: str, library_filter: str | None = None) -> ResolveResult:
    """Resolve a Kontakt instrument name.

    Note: Kontakt instruments are loaded via the Kontakt plugin, so this
    returns the instrument path for Kontakt to load (not directly insertable).

    Args:
        query: Fuzzy search query
        library_filter: Optional library name filter

    Returns:
        ResolveResult with the instrument path
    """
    results = search_kontakt(query, limit=5, library_filter=library_filter)

    if not results:
        return ResolveResult(
            success=False,
            spec=None,
            error=f"No Kontakt instrument found for '{query}'",
        )

    best = results[0]

    # For Kontakt, we return the .nki file path
    # The CLI/extension will need to handle this specially
    spec = DeviceSpec(
        type="file",  # Kontakt instruments are loaded as files
        path=best.file_path,
        display_name=f"{best.name} ({best.library})",
    )

    alternatives = [r.name for r in results[1:4]] if len(results) > 1 else None

    return ResolveResult(success=True, spec=spec, alternatives=alternatives)


def resolve_mtron(
    query: str,
    collection_filter: str | None = None,
    category_filter: str | None = None,
) -> ResolveResult:
    """Resolve an M-Tron patch name.

    Note: M-Tron patches are loaded via the M-Tron plugin.

    Args:
        query: Fuzzy search query
        collection_filter: Optional collection filter
        category_filter: Optional category filter

    Returns:
        ResolveResult with the patch path
    """
    results = search_mtron(
        query, limit=5, collection_filter=collection_filter, category_filter=category_filter
    )

    if not results:
        return ResolveResult(
            success=False,
            spec=None,
            error=f"No M-Tron patch found for '{query}'",
        )

    best = results[0]

    spec = DeviceSpec(
        type="file",
        path=best.file_path,
        display_name=f"{best.name} ({best.collection})",
    )

    alternatives = [r.name for r in results[1:4]] if len(results) > 1 else None

    return ResolveResult(success=True, spec=spec, alternatives=alternatives)


def resolve_device(query: str, hint: str | None = None) -> ResolveResult:
    """Resolve a device name with auto-detection.

    This function tries to intelligently determine what type of device
    the user is asking for based on the query and optional hint.

    Args:
        query: Fuzzy search query
        hint: Optional hint: "preset", "plugin", "kontakt", "mtron"

    Returns:
        ResolveResult with the resolved device
    """
    # If hint is provided, use the specific resolver
    if hint == "preset":
        return resolve_preset(query)
    elif hint == "plugin":
        return resolve_plugin(query)
    elif hint == "kontakt":
        return resolve_kontakt(query)
    elif hint == "mtron":
        return resolve_mtron(query)

    # Try to auto-detect based on the query
    # First, try as a preset (most common)
    result = resolve_preset(query)
    if result.success:
        return result

    # Then try as a plugin
    result = resolve_plugin(query)
    if result.success:
        return result

    # Finally return error
    return ResolveResult(
        success=False,
        spec=None,
        error=f"Could not find device matching '{query}'",
    )


def resolve_devices(
    specs: list[dict],
) -> tuple[list[DeviceSpec], list[str]]:
    """Resolve a list of device specifications.

    Each spec in the input can be:
    - {"query": "nektar piano"} - auto-detect
    - {"query": "reverb", "hint": "preset"} - force preset search
    - {"query": "kontakt", "hint": "plugin"} - force plugin search
    - {"type": "file", "path": "/path/to.bwpreset"} - already resolved

    Args:
        specs: List of device specifications to resolve

    Returns:
        Tuple of (resolved_specs, errors)
    """
    resolved: list[DeviceSpec] = []
    errors: list[str] = []

    for spec in specs:
        # Already resolved?
        if "type" in spec and "path" in spec:
            resolved.append(
                DeviceSpec(
                    type=spec["type"],
                    path=spec["path"],
                    display_name=spec.get("name", spec["path"]),
                )
            )
            continue

        # Need to resolve
        query = spec.get("query", "")
        hint = spec.get("hint")
        count = spec.get("count", 1)

        result = resolve_device(query, hint)

        if result.success and result.spec:
            # Add the device (possibly multiple times)
            for _ in range(count):
                resolved.append(result.spec)
        else:
            errors.append(result.error or f"Failed to resolve: {query}")

    return resolved, errors
