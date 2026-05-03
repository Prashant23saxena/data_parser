import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.odoo import model_fields


parser = argparse.ArgumentParser()
parser.add_argument("--connection", default="default")
parser.add_argument("--model", required=True)
args = parser.parse_args()

print(render_rows(model_fields(args.connection, args.model), columns=["name", "label", "type", "required", "relation"]))
