import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.odoo import fetch_records


parser = argparse.ArgumentParser()
parser.add_argument("--connection", default="default")
parser.add_argument("--model", required=True)
parser.add_argument("--fields", required=True)
parser.add_argument("--schema", required=True)
parser.add_argument("--table", required=True)
parser.add_argument("--limit", type=int, default=1000)
args = parser.parse_args()

fields = [field.strip() for field in args.fields.split(",") if field.strip()]
print(fetch_records(args.connection, args.model, fields, args.schema, args.table, limit=args.limit))
