import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.odoo import list_models


parser = argparse.ArgumentParser()
parser.add_argument("--connection", default="default")
parser.add_argument("--search")
args = parser.parse_args()

print(render_rows(list_models(args.connection, search=args.search), columns=["model", "name"]))
