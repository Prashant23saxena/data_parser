import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.execution import create_script


parser = argparse.ArgumentParser()
parser.add_argument("script")
parser.add_argument("--template", default="blank", choices=["blank", "join", "load-save"])
args = parser.parse_args()

created = create_script(args.script, template=args.template)
print(created["path"])
