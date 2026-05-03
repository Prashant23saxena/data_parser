import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.file_import import inspect_file


parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--sheet")
parser.add_argument("--limit", type=int, default=20)
parser.add_argument("--json", action="store_true")
args = parser.parse_args()

inspection = inspect_file(Path(args.file), preview_limit=args.limit, sheet=args.sheet)
if args.json:
    print(json.dumps(inspection, indent=2, default=str))
else:
    print(f"File: {inspection['fileName']}")
    print(f"Rows: {inspection['rowCount']}")
    if inspection["sheetNames"]:
        print(f"Sheets: {', '.join(inspection['sheetNames'])}")
    print("Columns:")
    print(render_rows(inspection["columns"], columns=["sourceName", "targetName", "inferredType", "status"]))
    print("Preview:")
    print(render_rows(inspection["previewRows"]))
