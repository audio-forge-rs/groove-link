"""Preset search using filesystem and Spotlight index."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .search import fuzzy_match


# Device type classifications
INSTRUMENTS = {
    "Polymer", "Phase-4", "FM-4", "Polysynth", "Sampler", "Drum Machine",
    "E-Clap", "E-Cowbell", "E-Hat", "E-Kick", "E-Snare", "E-Tom",
    "Organ", "FM-4 Operator", "Wavetable",
    "Poly Grid", "Note Grid",  # Grid-based instruments
}
NOTE_FX = {
    "Note Delay", "Arpeggiator", "Multi-Note", "Note Echo", "Note Filter",
    "Note Harmonizer", "Note Latch", "Note Length", "Note MOD",
    "Note Pitch Shifter", "Note Receiver", "Note Velocity", "Transposition Map",
    "Diatonic Transposer", "Note FX Layer", "Note FX Selector",
}
AUDIO_FX = {
    "Delay+", "Delay-2", "Delay-4", "Reverb", "Convolution",
    "Compressor", "Dynamics", "Gate", "Peak Limiter", "Transient Control",
    "EQ+", "EQ-5", "EQ-2", "Ladder", "Resonator Bank",
    "Chorus", "Flanger", "Phaser", "Freq Shifter", "Pitch Shifter",
    "Distortion", "Amp", "Bit-8", "Treemonster",
    "Filter", "Comb", "DC Blocker",
    "Blur", "Dual Pan", "Stereo Width", "Mid-Side Split", "Multiband FX-2", "Multiband FX-3",
    "Tool", "Oscilloscope", "Spectrum Analyzer", "Replacer",
    "FX Grid", "FX Layer", "FX Selector", "Chain",
    "Rotary", "De-Esser", "Harmonic EQ",
}


def _get_device_type(device: str | None) -> str:
    """Determine if device is instrument, note_fx, or audio_fx."""
    if not device:
        return ""
    if device in INSTRUMENTS:
        return "inst"
    if device in NOTE_FX:
        return "note"
    if device in AUDIO_FX:
        return "fx"
    # Heuristics for unknown devices
    if "Grid" in device:
        if "FX" in device:
            return "fx"
        return "inst"  # Poly Grid, Note Grid variants
    if "Note" in device:
        return "note"
    if device.endswith("+") or device.endswith("-2") or device.endswith("-4"):
        return "fx"
    return ""


@dataclass
class PresetMatch:
    """A preset search result with metadata extracted from path."""

    name: str
    file_path: str
    package: str  # e.g., "Bitwig", "Bajaao"
    pack: str  # e.g., "Wundertuete Vol. 1"
    category: str | None  # Full path after pack, e.g., "Presets/Polymer"
    device: str | None  # Extracted device name, e.g., "Polymer"
    device_type: str  # "inst", "note", "fx", or ""
    score: float  # Match relevance score
    load_type: str = "file"  # How to load: always "file" for presets

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "package": self.package,
            "pack": self.pack,
            "category": self.category,
            "device": self.device,
            "device_type": self.device_type,
            "load_type": self.load_type,
        }


def _parse_preset_path(path: str) -> tuple[str, str, str, str | None, str | None]:
    """Extract metadata from preset file path.

    Path structures:
    .../installed-packages/5.0/{Package}/{Pack}/Presets/{Device}/{Name}.bwpreset
    .../installed-packages/5.0/{Package}/{Pack}/{Name}.bwpreset  (flat pack)
    .../Library/Presets/{Device}/{Name}.bwpreset

    Returns:
        (name, package, pack, category, device)
        - category: full path between pack and filename (e.g., "Presets/Polymer")
        - device: extracted device name when identifiable (e.g., "Polymer")
    """
    p = Path(path)
    name = p.stem  # Filename without extension

    parts = p.parts

    # Try to find installed-packages structure
    try:
        pkg_idx = parts.index("installed-packages")
        # installed-packages/5.0/Package/Pack/...
        if pkg_idx + 3 < len(parts):
            package = parts[pkg_idx + 2]  # After 5.0
            pack = parts[pkg_idx + 3]

            # Get everything between pack and filename as category
            remaining = parts[pkg_idx + 4 : -1]  # Between pack and filename
            category = "/".join(remaining) if remaining else None

            # Extract device from Presets/{Device}/ structure
            device = None
            if remaining and remaining[0] == "Presets" and len(remaining) >= 2:
                device = remaining[1]
            elif remaining:
                # Use last subdirectory as device hint
                device = remaining[-1]

            return name, package, pack, category, device
    except ValueError:
        pass

    # Try user Library structure
    try:
        lib_idx = parts.index("Library")
        if lib_idx + 2 < len(parts) and parts[lib_idx + 1] == "Presets":
            device = parts[lib_idx + 2]
            return name, "User", "User Library", device, device
    except ValueError:
        pass

    # Fallback: use parent directory as pack
    return name, "Unknown", p.parent.name, None, None


def find_presets_spotlight() -> Iterator[str]:
    """Find all .bwpreset files using Spotlight (mdfind).

    This is fast because it uses macOS Spotlight index.
    """
    try:
        result = subprocess.run(
            ["mdfind", "-name", "bwpreset"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.endswith(".bwpreset"):
                    yield line
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Fallback to find if mdfind not available
        yield from find_presets_filesystem()


def find_presets_filesystem() -> Iterator[str]:
    """Find presets using filesystem walk (slower fallback)."""
    search_paths = [
        Path.home() / "Library/Application Support/Bitwig/Bitwig Studio/installed-packages",
        Path.home() / "Documents/Bitwig Studio/Library/Presets",
        Path("/Applications/Bitwig Studio.app/Contents/Resources/Library"),
    ]

    for base in search_paths:
        if base.exists():
            for root, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".bwpreset"):
                        yield os.path.join(root, f)


def find_presets_user_library() -> Iterator[str]:
    """Find presets in user's Bitwig Library (not always indexed by Spotlight)."""
    user_lib = Path.home() / "Documents/Bitwig Studio/Library/Presets"
    if user_lib.exists():
        for root, _, files in os.walk(user_lib):
            for f in files:
                if f.endswith(".bwpreset"):
                    yield os.path.join(root, f)


def search_presets(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
) -> list[PresetMatch]:
    """Search for presets matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)

    Returns:
        List of PresetMatch sorted by relevance
    """
    results: list[PresetMatch] = []
    seen_paths: set[str] = set()

    # Combine Spotlight results with user library (which may not be indexed)
    from itertools import chain
    for path in chain(find_presets_spotlight(), find_presets_user_library()):
        # Skip duplicates
        if path in seen_paths:
            continue
        seen_paths.add(path)
        # Skip device-settings (default presets with UUID dirs)
        if "/device-settings/" in path:
            continue

        name, package, pack, category, device = _parse_preset_path(path)

        # Score based on name and device match (boost by device name)
        score = fuzzy_match(query, name, device)

        if score >= min_score:
            results.append(
                PresetMatch(
                    name=name,
                    file_path=path,
                    package=package,
                    pack=pack,
                    category=category,
                    device=device,
                    device_type=_get_device_type(device),
                    score=score,
                )
            )

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
