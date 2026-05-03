import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.execution import list_scripts


print(render_rows(list_scripts(), columns=["name", "size", "updatedAt"]))
