import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.catalog import truncate_table


parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument("--confirm", required=True)
args = parser.parse_args()

result = truncate_table(args.table, confirmation=args.confirm)
print(f"Truncated {result['qualifiedName']}")
