import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401

from kriyax_workbench.file_import import commit_import, inspect_file


parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--schema", required=True)
parser.add_argument("--table", required=True)
parser.add_argument("--sheet")
parser.add_argument("--columns-json")
parser.add_argument("--auto", action="store_true")
args = parser.parse_args()

file_path = Path(args.file)
if args.columns_json:
    columns = json.loads(Path(args.columns_json).read_text(encoding="utf-8"))
elif args.auto:
    inspection = inspect_file(file_path, sheet=args.sheet)
    if inspection["requiresRename"]:
        raise SystemExit("Duplicate target columns detected. Run file_inspect.py --json, edit mapping, then pass --columns-json.")
    columns = inspection["columns"]
else:
    raise SystemExit("Pass --auto or --columns-json.")

result = commit_import(file_path, args.schema, args.table, columns=columns, sheet=args.sheet)
print(f"Imported {result['qualifiedName']} ({result['rowCount']} rows, {result['columnCount']} columns)")
