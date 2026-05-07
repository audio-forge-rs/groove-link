"""Splice instrument library search."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .search import fuzzy_match

# File extensions and their type classification
SPLICE_EXTENSIONS = {
    ".zmulti": "patch",
    ".zpreset": "preset",
    ".zconfig": "config",
    ".spitfire": "sample",
}

# Extensions to index (skip .zconfig as they are internal metadata)
SEARCHABLE_EXTENSIONS = {".zmulti", ".zpreset", ".spitfire"}

DEFAULT_SPLICE_ROOT = Path("/Volumes/Lacie/splice-library")


@dataclass
class SpliceMatch:
    """A Splice instrument search result."""

    name: str
    file_path: str
    pack: str
    type: str  # patch, preset, sample
    score: float = field(default=0.0)
    load_type: str = "splice"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "pack": self.pack,
            "type": self.type,
            "load_type": self.load_type,
        }


def _humanize_name(stem: str, pack_name: str) -> str:
    """Convert a file stem into a human-readable name.

    Strips common pack prefixes and converts underscores to spaces.
    e.g. "LABS___Glass_Piano_Glass_Piano_North_Star" -> "North Star"
         "LABS_ECQ_Long_Evil" -> "Long Evil"
         "DEAD_DRUMS" -> "Dead Drums"
    """
    name = stem

    # Step 1: Strip uppercase-only prefix (e.g. "LABS___" or "LABS_ECQ_")
    parts = name.split("_")
    for i in range(len(parts) - 1, 0, -1):
        candidate = "_".join(parts[i:])
        prefix = "_".join(parts[:i])
        if len(candidate) >= 2 and prefix.replace("_", "").isupper():
            name = candidate
            break

    # Step 2: Strip pack name prefix from remainder
    # e.g. pack "LABS - Glass Piano" -> try stripping "Glass_Piano_" (possibly repeated)
    # Extract the descriptive part of pack name (after " - " if present)
    pack_desc = pack_name.split(" - ", 1)[-1] if " - " in pack_name else pack_name
    pack_prefix = pack_desc.replace(" ", "_")
    # Strip repeated pack prefixes (some files have it twice)
    while name.startswith(pack_prefix + "_") and len(name) > len(pack_prefix) + 1:
        name = name[len(pack_prefix) + 1:]

    # Convert underscores to spaces, collapse multiple spaces, and title-case
    name = name.replace("_", " ")
    name = " ".join(name.split())
    if name.isupper() or name.islower():
        name = name.title()

    return name


def _get_splice_type(path: Path) -> str:
    """Classify a file by its parent directory and extension."""
    ext = path.suffix.lower()
    # Use parent directory name as primary signal
    parent = path.parent.name
    # Version directories (v0.1.1) -> check grandparent
    if parent.startswith("v"):
        parent = path.parent.parent.name

    if parent == "Patches":
        return "patch"
    elif parent == "Presets":
        return "preset"
    elif parent == "Samples":
        return "sample"

    # Fallback to extension
    return SPLICE_EXTENSIONS.get(ext, "unknown")


def enumerate_splice_content(root: Path) -> Iterator[SpliceMatch]:
    """Walk the Splice library directory and yield all searchable items.

    Structure: root/{Pack Name}/{Patches,Presets,Samples}/[version/]{files}
    """
    if not root.is_dir():
        return

    for pack_dir in sorted(root.iterdir()):
        if not pack_dir.is_dir():
            continue

        pack_name = pack_dir.name

        # Skip the shared "INSTRUMENT Common" directory (no playable content)
        if pack_name == "INSTRUMENT Common":
            continue

        for file_path in pack_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in SEARCHABLE_EXTENSIONS:
                continue

            file_type = _get_splice_type(file_path)
            name = _humanize_name(file_path.stem, pack_name)

            yield SpliceMatch(
                name=name,
                file_path=str(file_path),
                pack=pack_name,
                type=file_type,
            )


def get_all_splice_content(root: Path | None = None) -> list[SpliceMatch]:
    """Get all Splice library content.

    Args:
        root: Content root directory. Defaults to /Volumes/Lacie/splice-library/

    Returns:
        List of SpliceMatch objects (unsorted, unscored)
    """
    return list(enumerate_splice_content(root or DEFAULT_SPLICE_ROOT))


def search_splice(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
    type_filter: str | None = None,
    pack_filter: str | None = None,
    root: Path | None = None,
) -> list[SpliceMatch]:
    """Search for Splice instruments matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)
        type_filter: Optional type filter (patch, preset, sample)
        pack_filter: Optional pack name filter
        root: Content root directory

    Returns:
        List of SpliceMatch sorted by relevance
    """
    content = get_all_splice_content(root)
    results: list[SpliceMatch] = []

    type_filter_lower = type_filter.lower() if type_filter else None
    pack_filter_lower = pack_filter.lower() if pack_filter else None

    for item in content:
        if type_filter_lower and item.type != type_filter_lower:
            continue

        if pack_filter_lower and pack_filter_lower not in item.pack.lower():
            continue

        # Score based on name and pack
        score = fuzzy_match(query, item.name, item.pack)

        if score >= min_score:
            item.score = score
            results.append(item)

    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
