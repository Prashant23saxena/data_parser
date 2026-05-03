import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.catalog import rename_table


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("new_table")
args = parser.parse_args()

result = rename_table(args.table, args.new_table)
print(f"Renamed to {result['qualifiedName']}")
