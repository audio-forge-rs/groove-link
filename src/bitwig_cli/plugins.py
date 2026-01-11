"""Audio plugin search using filesystem and Spotlight."""

from __future__ import annotations

import plistlib
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .search import fuzzy_match


@dataclass
class PluginMatch:
    """A plugin search result."""

    name: str
    file_path: str
    format: str  # vst3, au, clap, vst
    vendor: str
    version: str | None
    location: str  # "user" or "system"
    bundle_id: str | None = None
    score: float = field(default=0.0)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "format": self.format,
            "vendor": self.vendor,
            "version": self.version,
            "location": self.location,
        }


# Known plugin abbreviations -> full searchable names
# Many vendors use abbreviations for plugin filenames
PLUGIN_ABBREVIATIONS: dict[str, str] = {
    # Ample Sound instruments (A = Ample, letter codes for instrument)
    "AEBJ": "Ample Ethno Banjo",
    "AEUJ": "Ample Ethno Ukulele",
    "AGML": "Ample Guitar Martin",
    "AGMJ": "Ample Guitar Martin Jumbo",
    "AGLP": "Ample Guitar Les Paul",
    "AGSC": "Ample Guitar Stratocaster",
    "AGTC": "Ample Guitar Telecaster",
    "AGPF": "Ample Guitar PF",
    "AGTS": "Ample Guitar Taylor",
    "AGTH": "Ample Guitar Hellrazer",
    "AGVN": "Ample Guitar Van Halen",
    "AGFV": "Ample Guitar Flame Vintage",
    "ABPJ": "Ample Bass P",
    "ABJJ": "Ample Bass J",
    "ABUJ": "Ample Bass Upright",
    "ABYJ": "Ample Bass Yinyang",
    "ABAJ": "Ample Bass Acoustic",
    "AME": "Ample Metal Eclipse",
    "AMR": "Ample Metal Ray",
    "ABSS": "Ample Bass Steinberger",
    "ABSJ": "Ample Bass Stingray",
    # Add more as discovered
}


# Plugin format extensions
PLUGIN_FORMATS = {
    ".vst3": "vst3",
    ".component": "au",
    ".clap": "clap",
    ".vst": "vst",
}

# Plugin search paths
USER_PLUGIN_PATHS = [
    Path.home() / "Library/Audio/Plug-Ins/VST3",
    Path.home() / "Library/Audio/Plug-Ins/VST",
    Path.home() / "Library/Audio/Plug-Ins/Components",
    Path.home() / "Library/Audio/Plug-Ins/CLAP",
]

SYSTEM_PLUGIN_PATHS = [
    Path("/Library/Audio/Plug-Ins/VST3"),
    Path("/Library/Audio/Plug-Ins/VST"),
    Path("/Library/Audio/Plug-Ins/Components"),
    Path("/Library/Audio/Plug-Ins/CLAP"),
]


def _parse_info_plist(bundle_path: Path) -> tuple[str | None, str | None, str | None]:
    """Extract vendor, version, and bundle ID from plugin's Info.plist.

    Returns:
        (vendor, version, bundle_id) tuple
    """
    plist_path = bundle_path / "Contents" / "Info.plist"
    if not plist_path.exists():
        return None, None, None

    try:
        with open(plist_path, "rb") as f:
            plist = plistlib.load(f)

        bundle_id = plist.get("CFBundleIdentifier", "")

        # Try various keys for vendor/manufacturer
        vendor = None
        if "." in bundle_id:
            parts = bundle_id.split(".")
            if len(parts) >= 2:
                vendor = parts[1]  # com.VENDOR.plugin
                # Clean up common vendor names
                vendor = vendor.replace("-", " ").replace("_", " ").title()

        version = plist.get("CFBundleShortVersionString") or plist.get("CFBundleVersion")

        return vendor, version, bundle_id
    except Exception:
        return None, None, None


def _extract_plugin_name(path: Path) -> str:
    """Extract clean plugin name from bundle path."""
    name = path.stem
    # Remove common suffixes
    for suffix in [" VST3", " AU", " CLAP", "_x64", "_arm64"]:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def find_plugins_spotlight() -> Iterator[Path]:
    """Find audio plugins using Spotlight."""
    # Search for each format
    for ext in PLUGIN_FORMATS:
        try:
            result = subprocess.run(
                ["mdfind", f"kMDItemFSName == '*{ext}'"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line and any(line.endswith(e) for e in PLUGIN_FORMATS):
                        yield Path(line)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass


def find_plugins_filesystem() -> Iterator[Path]:
    """Find plugins using filesystem walk (fallback)."""
    all_paths = USER_PLUGIN_PATHS + SYSTEM_PLUGIN_PATHS

    for base in all_paths:
        if base.exists():
            for item in base.iterdir():
                if item.suffix in PLUGIN_FORMATS:
                    yield item


def _get_location(path: Path) -> str:
    """Determine if plugin is in user or system location."""
    path_str = str(path)
    if path_str.startswith(str(Path.home())):
        return "user"
    return "system"


def _get_format(path: Path) -> str:
    """Get plugin format from path extension."""
    return PLUGIN_FORMATS.get(path.suffix, "unknown")


def get_all_plugins() -> list[PluginMatch]:
    """Get all plugins from the system.

    Returns:
        List of PluginMatch objects (unsorted, unscored)
    """
    seen_paths: set[str] = set()
    plugins: list[PluginMatch] = []

    # Try Spotlight first, fall back to filesystem
    try:
        plugin_paths = list(find_plugins_spotlight())
        if not plugin_paths:
            plugin_paths = list(find_plugins_filesystem())
    except Exception:
        plugin_paths = list(find_plugins_filesystem())

    for path in plugin_paths:
        path_str = str(path)

        # Skip duplicates
        if path_str in seen_paths:
            continue
        seen_paths.add(path_str)

        # Skip non-plugin directories
        if path.suffix not in PLUGIN_FORMATS:
            continue

        name = _extract_plugin_name(path)
        vendor, version, bundle_id = _parse_info_plist(path)
        fmt = _get_format(path)
        location = _get_location(path)

        plugins.append(
            PluginMatch(
                name=name,
                file_path=path_str,
                format=fmt,
                vendor=vendor or "Unknown",
                version=version,
                location=location,
                bundle_id=bundle_id,
            )
        )

    return plugins


def search_plugins(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
    format_filter: str | None = None,
) -> list[PluginMatch]:
    """Search for plugins matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)
        format_filter: Optional format filter (vst3, au, clap)

    Returns:
        List of PluginMatch sorted by relevance
    """
    plugins = get_all_plugins()
    results: list[PluginMatch] = []

    for plugin in plugins:
        # Filter by format if specified
        if format_filter and plugin.format != format_filter:
            continue

        # Look up expanded name from abbreviation mapping
        expanded_name = PLUGIN_ABBREVIATIONS.get(plugin.name.upper(), "")

        # Score based on name and vendor
        score = fuzzy_match(query, plugin.name, plugin.vendor)

        # Also try matching against expanded name if available
        if expanded_name:
            expanded_score = fuzzy_match(query, expanded_name, plugin.vendor)
            score = max(score, expanded_score)

        if score >= min_score:
            plugin.score = score
            results.append(plugin)

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
