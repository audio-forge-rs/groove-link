"""M-Tron Pro IV tape/patch search."""

from __future__ import annotations

import re
import zlib
from dataclasses import dataclass, field
from pathlib import Path

from .search import fuzzy_match


@dataclass
class MTronMatch:
    """An M-Tron patch search result."""

    name: str
    file_path: str
    collection: str  # e.g., "The Streetly Tapes Vol 2"
    category: str  # e.g., "Brass", "Strings", "Voices"
    author: str | None
    timbres: list[str]  # e.g., ["Breathy", "Vibrato", "Hollow"]
    types: list[str]  # e.g., ["Artist Patch", "Dynamic", "Layered"]
    score: float = field(default=0.0)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "collection": self.collection,
            "category": self.category,
            "author": self.author,
            "timbres": self.timbres,
            "types": self.types,
        }


# M-Tron library file location
MTRON_LIB_PATH = Path.home() / "Library/Application Support/GForce/M-Tron Pro IV/UPB_md_lib.gforce"


def _extract_field(data: str, field: str, start: int) -> tuple[str, int]:
    """Extract a field value from the binary format.

    Format: field_name\x00\x01{len}\x05{value}\x00

    Returns:
        (value, end_position)
    """
    pattern = field + r"\x00\x01.\x05([^\x00]*)\x00"
    match = re.search(pattern, data[start:])
    if match:
        return match.group(1), start + match.end()
    return "", start


def _parse_mtron_library() -> list[MTronMatch]:
    """Parse the M-Tron library metadata file.

    The file is zlib-compressed and contains a custom binary format
    with patch metadata including name, collection, category, timbres, etc.

    Returns:
        List of MTronMatch objects (unsorted, unscored)
    """
    if not MTRON_LIB_PATH.exists():
        return []

    try:
        with open(MTRON_LIB_PATH, "rb") as f:
            compressed = f.read()

        data = zlib.decompress(compressed).decode("utf-8", errors="replace")
    except Exception:
        return []

    patches: list[MTronMatch] = []

    # Find each "Patch" marker and parse the following fields
    # Skip the header (MD_LIB marker)
    patch_starts = [m.start() for m in re.finditer(r"Patch\x00", data)]

    for i, start in enumerate(patch_starts):
        # Determine end of this patch entry
        end = patch_starts[i + 1] if i + 1 < len(patch_starts) else len(data)
        region = data[start:end]

        # Extract fields using the binary format pattern
        name, _ = _extract_field(region, "name", 0)
        author, _ = _extract_field(region, "author", 0)
        collection, _ = _extract_field(region, "collection", 0)
        category, _ = _extract_field(region, "category", 0)
        path, _ = _extract_field(region, "path", 0)

        # Extract timbres (timbres0, timbres1, etc.)
        timbres = []
        for j in range(10):
            val, _ = _extract_field(region, f"timbres{j}", 0)
            if val:
                timbres.append(val)

        # Extract types (types0, types1, etc.)
        types = []
        for j in range(10):
            val, _ = _extract_field(region, f"types{j}", 0)
            if val:
                types.append(val)

        if name:  # Only add if we got a name
            patches.append(
                MTronMatch(
                    name=name.strip(),
                    file_path=path.strip() if path else "",
                    collection=collection.strip().replace("_", " ") if collection else "Unknown",
                    category=category.strip() if category else "Unknown",
                    author=author.strip() if author else None,
                    timbres=timbres,
                    types=types,
                )
            )

    return patches


def get_all_mtron_patches() -> list[MTronMatch]:
    """Get all M-Tron patches.

    Returns:
        List of MTronMatch objects (unsorted, unscored)
    """
    return _parse_mtron_library()


def search_mtron(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
    collection_filter: str | None = None,
    category_filter: str | None = None,
) -> list[MTronMatch]:
    """Search for M-Tron patches matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)
        collection_filter: Optional collection/tape bank filter
        category_filter: Optional category filter (Strings, Brass, etc.)

    Returns:
        List of MTronMatch sorted by relevance
    """
    patches = get_all_mtron_patches()
    results: list[MTronMatch] = []

    collection_filter_lower = collection_filter.lower() if collection_filter else None
    category_filter_lower = category_filter.lower() if category_filter else None

    for patch in patches:
        # Filter by collection if specified
        if collection_filter_lower and collection_filter_lower not in patch.collection.lower():
            continue

        # Filter by category if specified
        if category_filter_lower and category_filter_lower not in patch.category.lower():
            continue

        # Score based on name and collection
        score = fuzzy_match(query, patch.name, patch.collection)

        # Boost if query matches category
        if query.lower() in patch.category.lower():
            score += 0.2

        # Boost if query matches any timbre
        for timbre in patch.timbres:
            if query.lower() in timbre.lower():
                score += 0.1
                break

        if score >= min_score:
            patch.score = score
            results.append(patch)

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
