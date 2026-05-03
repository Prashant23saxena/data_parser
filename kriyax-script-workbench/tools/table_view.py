import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.catalog import preview_table


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--limit", type=int, default=20)
args = parser.parse_args()

preview = preview_table(args.table, limit=args.limit)
print(render_rows(preview["rows"], columns=preview["columns"]))
