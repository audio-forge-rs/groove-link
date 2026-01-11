"""Preset search using filesystem and Spotlight index."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class PresetMatch:
    """A preset search result with metadata extracted from path."""

    name: str
    file_path: str
    package: str  # e.g., "Bitwig", "Bajaao"
    pack: str  # e.g., "Wundertuete Vol. 1"
    category: str | None  # Full path after pack, e.g., "Presets/Polymer"
    device: str | None  # Extracted device name, e.g., "Polymer"
    score: float  # Match relevance score

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "package": self.package,
            "pack": self.pack,
            "category": self.category,
            "device": self.device,
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


def _fuzzy_match(query: str, text: str) -> float:
    """Simple fuzzy match score. Returns 0-1, higher is better.

    Scoring:
    - Exact match (case insensitive): 1.0
    - Query is substring: 0.8
    - All query words present: 0.6
    - Partial word matches: 0.3 per match
    """
    query_lower = query.lower()
    text_lower = text.lower()

    # Exact match
    if query_lower == text_lower:
        return 1.0

    # Substring match
    if query_lower in text_lower:
        # Boost if at word boundary
        if re.search(rf"\b{re.escape(query_lower)}", text_lower):
            return 0.9
        return 0.8

    # Word matching
    query_words = query_lower.split()
    text_words = set(re.findall(r"\w+", text_lower))

    matches = sum(1 for qw in query_words if qw in text_words)
    if matches == len(query_words):
        return 0.6

    # Partial word matching
    partial_matches = sum(
        1 for qw in query_words if any(qw in tw for tw in text_words)
    )
    if partial_matches > 0:
        return 0.3 * (partial_matches / len(query_words))

    return 0.0


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

        # Build searchable text from all metadata
        search_text = f"{name} {package} {pack} {category or ''} {device or ''}"

        score = _fuzzy_match(query, search_text)

        if score >= min_score:
            results.append(
                PresetMatch(
                    name=name,
                    file_path=path,
                    package=package,
                    pack=pack,
                    category=category,
                    device=device,
                    score=score,
                )
            )

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
