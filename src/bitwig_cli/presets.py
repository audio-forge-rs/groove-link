"""Preset search using filesystem and Spotlight index."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


# Device type classifications
INSTRUMENTS = {
    "Polymer", "Phase-4", "FM-4", "Polysynth", "Sampler", "Drum Machine",
    "E-Clap", "E-Cowbell", "E-Hat", "E-Kick", "E-Snare", "E-Tom",
    "Organ", "FM-4 Operator", "Wavetable",
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

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "package": self.package,
            "pack": self.pack,
            "category": self.category,
            "device": self.device,
            "device_type": self.device_type,
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


def _fuzzy_match(query: str, name: str, device: str | None) -> float:
    """Fuzzy match score with device weighting and granular scoring.

    Scoring is designed to minimize ties:
    - Device exact match: +0.50
    - Device partial match: +0.30
    - Name exact match: +1.00
    - Name substring at word boundary: +0.60 + position bonus
    - Name substring anywhere: +0.40 + position bonus
    - Name word match: +0.30 + coverage bonus
    - Name partial word: +0.15 + coverage bonus
    - Length similarity bonus: up to +0.05
    """
    import random

    query_lower = query.lower()
    name_lower = name.lower()
    device_lower = (device or "").lower()

    score = 0.0

    # Device matching (high weight)
    if device_lower:
        if query_lower == device_lower:
            score += 0.50
        elif query_lower in device_lower or device_lower in query_lower:
            score += 0.30

    # Name matching with position-based bonuses for variety
    if query_lower == name_lower:
        score += 1.00
    elif query_lower in name_lower:
        pos = name_lower.find(query_lower)
        # Earlier position = slightly higher score
        position_bonus = 0.05 * (1 - pos / max(len(name_lower), 1))

        if re.search(rf"\b{re.escape(query_lower)}", name_lower):
            score += 0.60 + position_bonus
        else:
            score += 0.40 + position_bonus
    else:
        # Word matching
        query_words = query_lower.split()
        name_words = list(re.findall(r"\w+", name_lower))
        name_word_set = set(name_words)

        exact_matches = sum(1 for qw in query_words if qw in name_word_set)
        if exact_matches > 0:
            # Coverage bonus: what fraction of query words matched
            coverage = exact_matches / len(query_words)
            score += 0.30 * coverage

        # Partial word matching
        partial_matches = sum(
            1 for qw in query_words
            if any(qw in nw for nw in name_word_set) and qw not in name_word_set
        )
        if partial_matches > 0:
            coverage = partial_matches / len(query_words)
            score += 0.15 * coverage

    # Random jitter to randomize ties (±0.03)
    # Large enough to shuffle results with similar scores
    score += random.uniform(-0.03, 0.03)

    return min(score, 1.5)


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

    for path in find_presets_spotlight():
        # Skip device-settings (default presets with UUID dirs)
        if "/device-settings/" in path:
            continue

        name, package, pack, category, device = _parse_preset_path(path)

        # Score based on name and device match
        score = _fuzzy_match(query, name, device)

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
