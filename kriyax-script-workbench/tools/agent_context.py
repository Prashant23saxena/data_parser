import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401

from kriyax_workbench.context_pack import build_context, render_markdown


parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=10)
parser.add_argument("--json", action="store_true")
parser.add_argument("--output")
args = parser.parse_args()

context = build_context(limit=args.limit)
text = json.dumps(context, indent=2, default=str) + "\n" if args.json else render_markdown(context)
if args.output:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(output)
else:
    print(text, end="")
