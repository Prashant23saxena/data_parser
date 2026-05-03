import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.pipelines import set_enabled


parser = argparse.ArgumentParser()
parser.add_argument("pipeline_id")
parser.add_argument("enabled", choices=["true", "false"])
args = parser.parse_args()

print(set_enabled(args.pipeline_id, args.enabled == "true"))
