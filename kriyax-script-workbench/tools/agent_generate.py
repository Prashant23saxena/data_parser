import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.agent import generate_code


parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument("--save")
args = parser.parse_args()

result = generate_code(args.prompt, save_as=args.save)
if result["savedPath"]:
    print(f"saved: {result['savedPath']}")
print(result["code"])
