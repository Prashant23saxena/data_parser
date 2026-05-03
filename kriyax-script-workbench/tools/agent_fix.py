import argparse
from pathlib import Path

import _bootstrap  # noqa: F401

from kriyax_workbench.agent import correct_code


parser = argparse.ArgumentParser()
parser.add_argument("--script", required=True)
parser.add_argument("--traceback-file", required=True)
parser.add_argument("--save", action="store_true")
args = parser.parse_args()

result = correct_code(args.script, Path(args.traceback_file).read_text(encoding="utf-8"), save=args.save)
if result["savedPath"]:
    print(f"saved: {result['savedPath']}")
print(result["code"])
