import argparse
import json

import _bootstrap  # noqa: F401

from kriyax_workbench.db_viewer import connection_info, render_text


parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

info = connection_info()
print(json.dumps(info, indent=2, default=str) if args.json else render_text(info))
