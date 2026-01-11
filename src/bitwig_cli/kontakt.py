"""Kontakt library search using Native Instruments database."""

from __future__ import annotations

import sqlite3
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .search import fuzzy_match


@dataclass
class KontaktMatch:
    """A Kontakt instrument search result."""

    name: str
    file_path: str
    library: str  # Kontakt library name
    vendor: str | None
    category: str | None
    score: float = field(default=0.0)
    load_type: str = "kontakt"  # Loaded via Kontakt plugin

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.file_path,
            "library": self.library,
            "vendor": self.vendor,
            "category": self.category,
            "load_type": self.load_type,
        }


# Kontakt database locations (in order of preference)
KONTAKT_DB_PATHS = [
    Path.home() / "Library/Application Support/Native Instruments/Kontakt 8/komplete.db3",
    Path.home() / "Library/Application Support/Native Instruments/Kontakt 7/komplete.db3",
]

# NKI file search paths (fallback)
NKI_SEARCH_PATHS = [
    Path("/Library/Application Support/Native Instruments/Kontakt 8/Content"),
    Path("/Users/Shared"),
    Path.home() / "Documents/Native Instruments",
]


def _get_kontakt_db() -> Path | None:
    """Find the Kontakt database file."""
    for db_path in KONTAKT_DB_PATHS:
        if db_path.exists():
            return db_path
    return None


def _query_kontakt_db(db_path: Path) -> list[KontaktMatch]:
    """Query the Kontakt database for all instruments.

    Returns:
        List of KontaktMatch objects (unsorted, unscored)
    """
    instruments: list[KontaktMatch] = []

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        # Query sound info with content path
        # Note: file_name actually contains full path in this DB
        # k_content_path.alias contains the library display name
        cursor.execute("""
            SELECT
                s.name,
                s.vendor,
                p.alias as library,
                s.file_name,
                s.sub_path
            FROM k_sound_info s
            JOIN k_content_path p ON s.content_path_id = p.id
            WHERE s.file_ext = 'nki'
        """)

        for row in cursor.fetchall():
            name, vendor, library, file_path, sub_path = row

            instruments.append(
                KontaktMatch(
                    name=name or Path(file_path).stem,
                    file_path=file_path,
                    library=library or "Unknown",
                    vendor=vendor,
                    category=sub_path,
                )
            )

        conn.close()
    except sqlite3.Error:
        pass

    return instruments


def find_nki_spotlight() -> Iterator[str]:
    """Find NKI files using Spotlight (fallback)."""
    try:
        result = subprocess.run(
            ["mdfind", "-name", ".nki"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.endswith(".nki"):
                    yield line
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


def _parse_nki_path(path: str) -> tuple[str, str, str | None]:
    """Extract metadata from NKI file path.

    Returns:
        (name, library, category)
    """
    p = Path(path)
    name = p.stem

    # Try to extract library name from path
    parts = p.parts

    # Look for "Library" in path
    for i, part in enumerate(parts):
        if "Library" in part and i > 0:
            library = parts[i - 1] if i > 0 else part
            # Get category from remaining path
            remaining = parts[i + 1 : -1]
            category = "/".join(remaining) if remaining else None
            return name, library, category

    # Fallback: use parent as library
    return name, p.parent.name, None


def get_all_kontakt_instruments() -> list[KontaktMatch]:
    """Get all Kontakt instruments.

    Tries database first, falls back to Spotlight search.

    Returns:
        List of KontaktMatch objects (unsorted, unscored)
    """
    # Try database first
    db_path = _get_kontakt_db()
    if db_path:
        instruments = _query_kontakt_db(db_path)
        if instruments:
            return instruments

    # Fallback to Spotlight
    instruments: list[KontaktMatch] = []
    seen_paths: set[str] = set()

    for path in find_nki_spotlight():
        if path in seen_paths:
            continue
        seen_paths.add(path)

        name, library, category = _parse_nki_path(path)
        instruments.append(
            KontaktMatch(
                name=name,
                file_path=path,
                library=library,
                vendor=None,
                category=category,
            )
        )

    return instruments


def search_kontakt(
    query: str,
    limit: int = 20,
    min_score: float = 0.1,
    library_filter: str | None = None,
) -> list[KontaktMatch]:
    """Search for Kontakt instruments matching the query.

    Args:
        query: Search query (case insensitive, fuzzy)
        limit: Maximum number of results
        min_score: Minimum match score (0-1)
        library_filter: Optional library name filter

    Returns:
        List of KontaktMatch sorted by relevance
    """
    instruments = get_all_kontakt_instruments()
    results: list[KontaktMatch] = []

    library_filter_lower = library_filter.lower() if library_filter else None

    for inst in instruments:
        # Filter by library if specified
        if library_filter_lower and library_filter_lower not in inst.library.lower():
            continue

        # Score based on name and library
        score = fuzzy_match(query, inst.name, inst.library)

        if score >= min_score:
            inst.score = score
            results.append(inst)

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, m.name.lower()))

    return results[:limit]
