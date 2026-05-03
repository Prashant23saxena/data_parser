import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.odoo import save_connection


parser = argparse.ArgumentParser()
parser.add_argument("--name", default="default")
parser.add_argument("--url", required=True)
parser.add_argument("--database", required=True)
parser.add_argument("--username", required=True)
parser.add_argument("--api-key", required=True)
args = parser.parse_args()

print(save_connection(vars(args)))
