import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.pipelines import list_pipelines


print(render_rows(list_pipelines(), columns=["id", "name", "script", "enabled"]))
