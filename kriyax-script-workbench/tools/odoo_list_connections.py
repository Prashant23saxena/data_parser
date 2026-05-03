import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.odoo import list_connections


print(render_rows(list_connections(), columns=["name", "url", "database", "username", "updatedAt"]))
