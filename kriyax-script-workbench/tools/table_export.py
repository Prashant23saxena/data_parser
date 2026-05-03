import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.catalog import export_table, export_table_html


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--output")
parser.add_argument("--format", choices=["csv", "html"], default="csv")
parser.add_argument("--limit", type=int, default=100)
args = parser.parse_args()

if args.format == "html":
    print(export_table_html(args.table, output_path=args.output, limit=args.limit))
else:
    print(export_table(args.table, output_path=args.output))
