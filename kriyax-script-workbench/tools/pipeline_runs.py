import argparse

import _bootstrap  # noqa: F401

from _format import render_rows
from kriyax_workbench.pipelines import list_runs


parser = argparse.ArgumentParser()
parser.add_argument("--pipeline")
parser.add_argument("--status", default="all")
args = parser.parse_args()

print(render_rows(list_runs(pipeline_id=args.pipeline, status=args.status), columns=["id", "pipelineName", "status", "trigger", "startedAt"]))
