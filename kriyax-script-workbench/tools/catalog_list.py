import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.catalog import list_tables


if __name__ == "__main__":
    rows = list_tables()
    print(render_rows(rows, columns=["qualifiedName", "rowCount", "columnCount"]))
