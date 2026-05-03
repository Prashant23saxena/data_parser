from __future__ import annotations

from typing import Any


def render_rows(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "No rows."
    selected = columns or list(rows[0].keys())
    widths = {column: max(len(column), *(len(str(row.get(column, ""))) for row in rows)) for column in selected}
    header = "  ".join(column.ljust(widths[column]) for column in selected)
    rule = "  ".join("-" * widths[column] for column in selected)
    body = ["  ".join(str(row.get(column, "")).ljust(widths[column]) for column in selected) for row in rows]
    return "\n".join([header, rule, *body])
