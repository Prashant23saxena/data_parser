import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.odoo import sync_cursor


parser = argparse.ArgumentParser()
parser.add_argument("cursor_id")
parser.add_argument("--limit", type=int, default=1000)
args = parser.parse_args()

print(sync_cursor(args.cursor_id, limit=args.limit))
