import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.pipelines import list_failures


print(render_rows(list_failures(), columns=["runId", "pipelineName", "status", "createdAt"]))
