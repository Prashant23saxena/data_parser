import argparse
import json

import _bootstrap  # noqa: F401

from kriyax_workbench.audit import get_event


parser = argparse.ArgumentParser()
parser.add_argument("event_id")
args = parser.parse_args()

print(json.dumps(get_event(args.event_id), indent=2, default=str))
