import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.pipelines import set_schedule


parser = argparse.ArgumentParser()
parser.add_argument("pipeline_id")
parser.add_argument("--hourly", action="store_true")
parser.add_argument("--daily")
args = parser.parse_args()

schedule = {"type": "hourly"} if args.hourly or not args.daily else {"type": "daily", "timeOfDay": args.daily}
print(set_schedule(args.pipeline_id, schedule))
