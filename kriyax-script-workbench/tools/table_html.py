import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.catalog import export_table_html


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--output")
parser.add_argument("--limit", type=int, default=100)
args = parser.parse_args()

print(export_table_html(args.table, output_path=args.output, limit=args.limit))
