import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.agent import follow_up


parser = argparse.ArgumentParser()
parser.add_argument("--script", required=True)
parser.add_argument("request")
parser.add_argument("--save", action="store_true")
args = parser.parse_args()

result = follow_up(args.script, args.request, save=args.save)
if result["savedPath"]:
    print(f"saved: {result['savedPath']}")
print(result["code"])
