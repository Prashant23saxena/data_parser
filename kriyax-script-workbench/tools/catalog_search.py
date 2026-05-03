import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.catalog import search_tables


parser = argparse.ArgumentParser()
parser.add_argument("query")
args = parser.parse_args()

print(render_rows(search_tables(args.query), columns=["qualifiedName", "rowCount", "columnCount"]))
