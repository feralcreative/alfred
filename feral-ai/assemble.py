#!/usr/bin/env python3
"""Assemble a Feral AI prompt: read a template, substitute {{TOKEN}} tokens
from the environment variables set by the prompt chain, print the result.

Invoked by the workflow's final Run Script action as:
    assemble.py prompts/<name>.txt

Tokens are substituted from environment variables of the same name, plus one
computed token:
    {{EXCHANGE_TICKER}} -> "<EXCHANGE>: <TICKER>" when both are present,
                           otherwise "private".

The assembled text is printed to stdout, which becomes {query} for the
downstream Clipboard output object.
"""

import os
import re
import sys

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def resolve(token):
    if token == "EXCHANGE_TICKER":
        exchange = os.environ.get("EXCHANGE", "").strip()
        ticker = os.environ.get("TICKER", "").strip()
        if exchange and ticker:
            return f"{exchange}: {ticker}"
        return "private"
    return os.environ.get(token, "").strip()


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: assemble.py <template-path>\n")
        sys.exit(1)

    template_path = sys.argv[1]
    if not os.path.isfile(template_path):
        sys.stderr.write(f"template not found: {template_path}\n")
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    filled = TOKEN_RE.sub(lambda m: resolve(m.group(1)), template)
    sys.stdout.write(filled.strip("\n"))


if __name__ == "__main__":
    main()
