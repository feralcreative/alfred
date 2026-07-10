#!/usr/bin/env python3
"""Generic per-field Script Filter for the Feral AI prompt chain.

One instance runs for each field being collected (company, exchange, ...).
The build script bakes the field metadata into the invocation; the user's typed
text arrives as the positional `query` argument. We emit a single Alfred item
whose `variables` set THIS field's variable — Alfred merges item variables into
the flow when the item is actioned, so prior fields carry forward automatically.

Contract:
  prompt-field.py --var VAR --label LABEL --hint HINT --required 0|1
                  --prior VAR1,VAR2 -- "<query>"

Empty query:
  * required field  -> item invalid (Enter is a no-op until the user types)
  * optional field  -> item valid, variable set to "" (renders downstream as
                       "private" for the exchange/ticker pair)
"""

import argparse
import json
import os
import sys


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--var", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--hint", default="")
    p.add_argument("--required", type=int, default=0)
    p.add_argument("--prior", default="")
    p.add_argument("query", nargs="?", default="")
    return p.parse_args(argv)


def prior_summary(prior_names):
    """Human-readable recap of already-collected fields, read from env."""
    parts = []
    for name in [n for n in prior_names.split(",") if n]:
        val = os.environ.get(name, "").strip()
        parts.append(f"{name.title()}: {val or '—'}")
    return "   ·   ".join(parts)


def main():
    args = parse_args(sys.argv[1:])
    query = args.query.strip()
    recap = prior_summary(args.prior)

    if query:
        title = query
        subtitle = args.hint
        valid = True
        value = query
    elif args.required:
        title = f"Type the {args.label.lower()}…"
        subtitle = args.hint
        valid = False
        value = ""
    else:
        title = f"Leave blank — {args.label.lower()} not applicable (private)"
        subtitle = args.hint
        valid = True
        value = ""

    if recap:
        subtitle = f"{subtitle}      [ {recap} ]" if subtitle else f"[ {recap} ]"

    item = {
        "uid": args.var,
        "title": title,
        "subtitle": subtitle,
        # arg MUST be empty: Alfred pre-fills the next chained Script Filter's
        # search box with the actioned item's arg. The field's value is carried
        # forward in `variables` (read from the environment by assemble.py), so
        # arg only needs to clear the box for the next prompt.
        "arg": "",
        "valid": valid,
        "variables": {args.var: value},
    }
    print(json.dumps({"items": [item]}))


if __name__ == "__main__":
    main()
