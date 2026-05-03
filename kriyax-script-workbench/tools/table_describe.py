import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.catalog import describe_table


parser = argparse.ArgumentParser()
parser.add_argument("table")
args = parser.parse_args()

description = describe_table(args.table)
print(f"Table: {description['qualifiedName']}")
print(f"Rows: {description['rowCount']}")
print(render_rows(description["columns"], columns=["name", "type"]))
