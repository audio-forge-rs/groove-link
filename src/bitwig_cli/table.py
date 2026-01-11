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
    max_total_width: int = 100,
) -> Table:
    """Create a table with columns sized to fit content.

    Args:
        rows: List of data objects
        columns: Column definitions
        title: Optional table title
        max_total_width: Maximum total table width

    Returns:
        Rich Table with adaptive column widths
    """
    if not rows:
        table = Table(title=title, show_header=True, header_style="bold")
        for col in columns:
            table.add_column(col.name)
        return table

    # Calculate content widths for each column
    col_widths: list[int] = []
    col_values: list[list[str]] = []

    for col in columns:
        values = [col.get_value(row) for row in rows]
        col_values.append(values)

        # Width = max of header and content, bounded by min/max
        max_content = max(len(v) for v in values) if values else 0
        width = max(len(col.name), max_content)
        width = max(col.min_width, min(col.max_width, width))
        col_widths.append(width)

    # If total exceeds max, shrink lower priority columns first
    total = sum(col_widths) + (len(columns) * 3)  # Account for separators
    if total > max_total_width:
        overflow = total - max_total_width

        # Sort columns by priority (lower first) for shrinking
        shrink_order = sorted(range(len(columns)), key=lambda i: columns[i].priority)

        for i in shrink_order:
            if overflow <= 0:
                break
            col = columns[i]
            shrinkable = col_widths[i] - col.min_width
            shrink = min(shrinkable, overflow)
            col_widths[i] -= shrink
            overflow -= shrink

    # Create table
    table = Table(title=title, show_header=True, header_style="bold")
    for col, width in zip(columns, col_widths):
        table.add_column(col.name, width=width, no_wrap=True)

    # Add rows with truncated values
    for row_idx, row in enumerate(rows):
        table.add_row(*[
            col_values[col_idx][row_idx][:col_widths[col_idx]]
            for col_idx in range(len(columns))
        ])

    return table
