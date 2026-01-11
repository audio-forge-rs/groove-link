"""Adaptive table utilities for CLI output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from rich.console import Console
from rich.table import Table


@dataclass
class Column:
    """Column definition with optional value extractor."""

    name: str
    key: str | Callable[[Any], str] | None = None  # Attribute name or callable
    min_width: int = 4
    max_width: int = 40
    priority: int = 1  # Higher = keep width when shrinking

    def get_value(self, row: Any) -> str:
        """Extract string value from row."""
        if self.key is None:
            # Use column name as attribute
            val = getattr(row, self.name.lower(), "")
        elif callable(self.key):
            val = self.key(row)
        else:
            val = getattr(row, self.key, "")
        return str(val) if val else ""


def adaptive_table(
    rows: list[Any],
    columns: list[Column],
    title: str | None = None,
) -> Table:
    """Create a table with columns sized to fit ALL content. Never truncates.

    Args:
        rows: List of data objects
        columns: Column definitions
        title: Optional table title

    Returns:
        Rich Table with columns wide enough for all content
    """
    if not rows:
        table = Table(title=title, show_header=True, header_style="bold")
        for col in columns:
            table.add_column(col.name)
        return table

    # Calculate content widths for each column - use actual max width needed
    col_values: list[list[str]] = []

    for col in columns:
        values = [col.get_value(row) for row in rows]
        col_values.append(values)

    # Create table - no truncation, columns size to content
    # width=None removes the terminal width constraint
    table = Table(title=title, show_header=True, header_style="bold", width=None)
    for col in columns:
        table.add_column(col.name, no_wrap=True)

    # Add rows with FULL values - no truncation
    for row_idx, _row in enumerate(rows):
        table.add_row(*[
            col_values[col_idx][row_idx]
            for col_idx in range(len(columns))
        ])

    return table
