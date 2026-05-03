import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.odoo import create_cursor


parser = argparse.ArgumentParser()
parser.add_argument("--connection", default="default")
parser.add_argument("--model", required=True)
parser.add_argument("--fields", required=True)
parser.add_argument("--schema", required=True)
parser.add_argument("--table", required=True)
parser.add_argument("--cursor-field", default="write_date")
args = parser.parse_args()

fields = [field.strip() for field in args.fields.split(",") if field.strip()]
print(create_cursor(args.connection, args.model, fields, args.schema, args.table, cursor_field=args.cursor_field))
