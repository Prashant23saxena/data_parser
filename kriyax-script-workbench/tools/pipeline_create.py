import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.pipelines import create_pipeline


parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--script", required=True)
parser.add_argument("--connector-sync-id")
args = parser.parse_args()

print(create_pipeline(args.name, args.script, connector_sync_id=args.connector_sync_id))
