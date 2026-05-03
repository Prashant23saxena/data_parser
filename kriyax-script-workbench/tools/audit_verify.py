import argparse
import json

import _bootstrap  # noqa: F401

from kriyax_workbench.audit import verify_snapshot


parser = argparse.ArgumentParser()
parser.add_argument("event_id")
args = parser.parse_args()

print(json.dumps(verify_snapshot(args.event_id), indent=2, default=str))
