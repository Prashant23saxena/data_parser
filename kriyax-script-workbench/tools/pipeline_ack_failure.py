import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.pipelines import acknowledge_failure


parser = argparse.ArgumentParser()
parser.add_argument("run_id")
args = parser.parse_args()

print(acknowledge_failure(args.run_id))
