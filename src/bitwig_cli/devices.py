"""Bitwig base device search using filesystem and Spotlight index."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .search import fuzzy_match


# Device category classifications for base Bitwig devices
INSTRUMENTS = {
    "Polymer", "Phase-4", "FM-4", "Polysynth", "Sampler", "Drum Machine",
    "E-Clap", "E-Cowbell", "E-Hat", "E-Kick", "E-Snare", "E-Tom",
    "Organ", "Wavetable", "Poly Grid", "Note Grid",
    "Instrument Layer", "Instrument Selector",
    # Drum/percussion elements
    "v0 Clap", "v0 Cowbell", "v0 Cymbal", "v0 Hat Closed", "v0 Hat Open",
    "v0 Kick", "v0 Snare", "v0 Tom",
    "v8 Clap", "v8 Cowbell", "v8 Cymbal", "v8 Hat Closed", "v8 Hat Open",
    "v8 Kick", "v8 Snare", "v8 Tom",
    "v9 Clap", "v9 Cowbell", "v9 Cymbal", "v9 Hat Closed", "v9 Hat Open",
    "v9 Kick", "v9 Snare", "v9 Tom",
}

NOTE_FX = {
    "Arpeggiator", "Diatonic Transposer", "Harmonize", "Humanize",
    "Multi-note", "Note Delay", "Note Echo", "Note Filter",
    "Note FX Layer", "Note FX Selector", "Note Harmonizer",
    "Note Latch", "Note Length", "Note MOD", "Note Pitch Shifter",
    "Note Receiver", "Note Repeats", "Note Transpose", "Note Velocity",
    "Transposition Map", "Velocity Curve",
}

AUDIO_FX = {
    # Dynamics
    "Compressor", "Compressor+", "Dynamics", "Gate", "Peak Limiter", "Transient Control",
    "De-Esser", "Loudness",
    # EQ/Filter
    "EQ+", "EQ-5", "EQ-2", "Ladder", "Filter", "Comb", "DC Blocker",
    "Resonator Bank", "Harmonic EQ", "Freq Shifter",
    # Delay/Reverb
    "Delay+", "Delay-2", "Delay-4", "Reverb", "Convolution",
    # Modulation
    "Chorus", "Flanger", "Phaser", "Rotary", "Pitch Shifter",
    "Ring-Mod", "Blur",
    # Distortion
    "Distortion", "Amp", "Bit-8", "Treemonster", "Cabinet",
    # Utility FX
    "Dual Pan", "Stereo Width", "Mid-Side Split",
    "FX Grid", "FX Layer", "FX Selector", "Chain",
    # Analysis
    "Tool", "Oscilloscope", "Spectrum Analyzer", "Replacer",
    # Multi
    "Multiband FX-2", "Multiband FX-3",
}

ROUTING = {
    "Audio Receiver", "Note Receiver",
    "Audio Sidechain", "HW Clock Out",
    "HW CV Instrument", "HW CV Out", "HW Instrument", "HW FX",
}

MODULATORS = {
    "ADSR", "AHDSR", "Audio MOD", "Audio Rate", "Audio Sidechain",
    "Beat LFO", "Bounce", "Button", "Classic LFO", "Envelope Follower",
    "Expressions", "Focus", "Keytrack", "LFO", "Macro-4",
    "Math", "MIDI CC", "MIDI Velocity", "Mini LFO",
    "Mix", "Note Sidechain", "Polynom", "Random",
    "Select-4", "Steps", "Step MOD", "Sweep", "Vector-4", "Vector-8",
    "XY",
}

UTILITY = {
    "DC Offset", "Test Tone", "Stereo Split",
}


def _get_device_category(name: str) -> str:
    """Determine device category from name."""
    if name in INSTRUMENTS:
        return "inst"
    if name in NOTE_FX:
        return "note"
    if name in AUDIO_FX:
        return "fx"
    if name in ROUTING:
        return "routing"
    if name in MODULATORS:
        return "mod"
    if name in UTILITY:
        return "util"
    # Heuristics
    if "Grid" in name:
        if "FX" in name:
            return "fx"
        if "Note" in name:
            return "note"
        return "inst"
    if "Note" in name:
        return "note"
    if name.startswith("v0 ") or name.startswith("v8 ") or name.startswith("v9 "):
        return "inst"  # Drum elements
    if name.startswith("HW "):
        return "routing"
    return ""


@dataclass
class DeviceMatch:
    """A base device search result."""

    name: str
    file_path: str
    category: str  # "inst", "note", "fx", "routing", "mod", "util", ""
    score: float
    load_type: str = "device"  # How to load: "device" for base devices

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "category": self.category,
            "load_type": self.load_type,
        }


def find_devices() -> Iterator[str]:
    """Find all .bwdevice files.

    Uses filesystem search since Spotlight doesn't index app bundles.
    """
    yield from find_devices_filesystem()


def find_devices_filesystem() -> Iterator[str]:
    """Find devices using filesystem walk (slower fallback)."""
    search_paths = [
        Path("/Applications/Bitwig Studio.app/Contents/Resources/Library/devices"),
        # User-installed devices could go here in future
        Path.home() / "Documents/Bitwig Studio/Library/devices",
    ]

    for base in search_paths:
        if base.exists():
            for root, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".bwdevice"):
                        yield os.path.join(root, f)


def search_devices(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
    category_filter: str | None = None,
) -> list[DeviceMatch]:
    """Search for Bitwig base devices matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)
        category_filter: Filter by category: "inst", "note", "fx", "routing", "mod", "util"

    Returns:
        List of DeviceMatch sorted by relevance
    """
    results: list[DeviceMatch] = []
    seen_paths: set[str] = set()

    for path in find_devices():
        # Skip duplicates
        if path in seen_paths:
            continue
        seen_paths.add(path)

        # Extract device name from filename
        name = Path(path).stem
        category = _get_device_category(name)

        # Apply category filter if specified
        if category_filter and category != category_filter:
            continue

        # Score based on name match
        score = fuzzy_match(query, name)

        if score >= min_score:
            results.append(
                DeviceMatch(
                    name=name,
                    file_path=path,
                    category=category,
                    score=score,
                )
            )

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
