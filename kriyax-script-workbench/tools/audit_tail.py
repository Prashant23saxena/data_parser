import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.audit import read_events


parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=20)
args = parser.parse_args()

events = read_events(limit=args.limit)
print(render_rows(events, columns=["createdAt", "eventType", "status", "scriptName", "savedTables"]))
