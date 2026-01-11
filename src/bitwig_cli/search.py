"""Shared search utilities for CLI commands."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Callable, Protocol, TypeVar


@dataclass
class SearchMatch:
    """Base class for search results."""

    name: str
    file_path: str
    score: float

    def to_dict(self) -> dict:
        """Override in subclasses for specific fields."""
        return {"name": self.name, "path": self.file_path}


T = TypeVar("T", bound=SearchMatch)


class Searchable(Protocol):
    """Protocol for searchable items."""

    name: str
    score: float


def fuzzy_match(
    query: str,
    name: str,
    boost_field: str | None = None,
) -> float:
    """Fuzzy match score with optional boost field.

    Scoring is designed to minimize ties:
    - Boost field exact match: +0.50
    - Boost field partial match: +0.30
    - Name exact match: +1.00
    - Name substring at word boundary: +0.60 + position bonus
    - Name substring anywhere: +0.40 + position bonus
    - Name word match: +0.30 + coverage bonus
    - Name partial word: +0.15 + coverage bonus
    - Random jitter: ±0.03 (to shuffle ties)

    Args:
        query: Search query (case insensitive)
        name: Item name to match against
        boost_field: Optional field to boost matches (e.g., device name, vendor)

    Returns:
        Match score (0.0 to ~1.5)
    """
    query_lower = query.lower()
    name_lower = name.lower()
    boost_lower = (boost_field or "").lower()

    score = 0.0

    # Boost field matching (high weight)
    if boost_lower:
        if query_lower == boost_lower:
            score += 0.50
        elif query_lower in boost_lower or boost_lower in query_lower:
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
            1
            for qw in query_words
            if any(qw in nw for nw in name_word_set) and qw not in name_word_set
        )
        if partial_matches > 0:
            coverage = partial_matches / len(query_words)
            score += 0.15 * coverage

    # Random jitter to randomize ties (±0.03)
    score += random.uniform(-0.03, 0.03)

    return min(score, 1.5)


def search_and_rank(
    items: list[T],
    query: str,
    get_name: Callable[[T], str],
    get_boost: Callable[[T], str | None] | None = None,
    min_score: float = 0.1,
    limit: int = 20,
) -> list[T]:
    """Search items and return ranked results.

    Args:
        items: List of items to search
        query: Search query
        get_name: Function to extract name from item
        get_boost: Optional function to extract boost field from item
        min_score: Minimum score threshold
        limit: Maximum results to return

    Returns:
        Sorted list of matching items with scores
    """
    results = []

    for item in items:
        name = get_name(item)
        boost = get_boost(item) if get_boost else None
        score = fuzzy_match(query, name, boost)

        if score >= min_score:
            # Create a copy with the score set
            item.score = score
            results.append(item)

    # Sort by score (descending), then by name
    results.sort(key=lambda m: (-m.score, get_name(m).lower()))

    return results[:limit]
