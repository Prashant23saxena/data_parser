import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.execution import read_script


parser = argparse.ArgumentParser()
parser.add_argument("script")
args = parser.parse_args()

print(read_script(args.script)["code"])
