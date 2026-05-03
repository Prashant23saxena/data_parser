import argparse

import _bootstrap  # noqa: F401

from kriyax_workbench.execution import run_script


parser = argparse.ArgumentParser()
parser.add_argument("script")
args = parser.parse_args()

result = run_script(args.script)
print(f"status: {result['status']}")
print(f"script: {result['scriptName']}")
if result["stdout"]:
    print("stdout:")
    print(result["stdout"])
if result["stderr"]:
    print("stderr:")
    print(result["stderr"])
if result["displayFrames"]:
    print("previews:")
    for frame in result["displayFrames"]:
        print(f"- {frame['name']} ({frame['rowCount']} rows)")
if result["savedTables"]:
    print("saved tables:")
    for table in result["savedTables"]:
        print(f"- {table}")
