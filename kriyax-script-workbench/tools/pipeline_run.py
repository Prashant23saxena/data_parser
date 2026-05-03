import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.pipelines import run_pipeline


parser = argparse.ArgumentParser()
parser.add_argument("pipeline_id")
args = parser.parse_args()

print(run_pipeline(args.pipeline_id))
