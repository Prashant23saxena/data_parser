import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.llm import complete_text


parser = argparse.ArgumentParser()
parser.add_argument("prompt")
args = parser.parse_args()

print(complete_text(args.prompt))
