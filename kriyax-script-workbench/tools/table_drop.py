import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.catalog import drop_table


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--confirm", required=True)
args = parser.parse_args()

result = drop_table(args.table, confirmation=args.confirm)
print(f"Dropped {result['qualifiedName']}")
