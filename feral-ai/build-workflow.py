#!/usr/bin/env python3
"""Build the Feral AI Alfred workflow from prompts.json.

Each prompt becomes a chain of objects:

    [keyword] SF(field 1) -> SF(field 2) -> ... -> SF(field N)
        -> Run Script (assemble.py <template>)
        -> Clipboard output ({query})
        -> Notification

Alfred chains Script Filters: actioning an item runs the next connected Script
Filter with the freshly-typed text as its query, and item `variables` merge into
the flow. So each field's Script Filter only sets its own variable; prior fields
carry forward automatically. The final Run Script reads all collected variables
from the environment, substitutes them into the template, and prints the result,
which the Clipboard output copies.

Edit prompts.json (and the referenced template files) and run ./rebuild.sh.
"""

import json
import os
import plistlib
import re
import shlex
import sys
import uuid

PROMPTS_FILE = "prompts.json"
DEFAULT_VERSION = "1.0"


def get_current_version() -> str:
    """Read version from existing info.plist; fall back to DEFAULT_VERSION."""
    if not os.path.exists("info.plist"):
        return DEFAULT_VERSION
    try:
        with open("info.plist", "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(
            r"<key>variablesdontexport</key>.*?<key>version</key>\s*<string>([^<]+)</string>",
            content,
            re.DOTALL,
        )
        if match:
            return match.group(1)
    except OSError as e:
        print(f"Warning: could not read current version: {e}")
    return DEFAULT_VERSION


def increment_version(current: str, major: bool = False) -> str:
    try:
        v = float(current)
        if major:
            major_part = int(v)
            minor_part = int((v - major_part) * 100)
            if minor_part == 0:
                return f"{major_part}.1"
            new_minor = ((minor_part // 10) + 1) * 10
            return f"{major_part + 1}.0" if new_minor >= 100 else f"{major_part}.{new_minor}"
        return f"{v + 0.01:.2f}"
    except ValueError:
        print(f"Warning: invalid version '{current}', defaulting to {DEFAULT_VERSION}")
        return DEFAULT_VERSION


def new_uid() -> str:
    return str(uuid.uuid4()).upper()


def create_script_filter(field: dict, keyword: str, prior: list[str]) -> dict:
    """A Script Filter that collects one field.

    config mirrors the proven port-roulette Script Filter (arg passing, escaping,
    queue behaviour); only keyword/script/title/subtext change. `keyword` is empty
    for mid-chain filters — they are reached via connection, not typed directly.
    """
    script = (
        "/usr/bin/python3 ./prompt-field.py "
        f"--var {shlex.quote(field['var'])} "
        f"--label {shlex.quote(field['label'])} "
        f"--hint {shlex.quote(field.get('hint', ''))} "
        f"--required {1 if field.get('required') else 0} "
        f"--prior {shlex.quote(','.join(prior))} "
        '"$1"'
    )
    return {
        "config": {
            "alfredfiltersresults": False,
            "alfredfiltersresultsmatchmode": 0,
            "argumenttrimmode": 0,
            "argumenttype": 1,
            "escaping": 102,
            "keyword": keyword,
            "queuedelaycustom": 3,
            "queuedelayimmediatelyinitially": False,
            "queuedelaymode": 0,
            "queuemaxsize": 1,
            "runningsubtext": "",
            "script": script,
            "scriptargtype": 1,
            "scriptfile": "",
            "subtext": field.get("hint", ""),
            "title": field["label"],
            "type": 0,
            "withspace": True,
        },
        "type": "alfred.workflow.input.scriptfilter",
        "uid": new_uid(),
        "version": 3,
    }


def create_assemble_action(template: str) -> dict:
    """Run Script that fills the template from env vars and prints the result."""
    script = f"/usr/bin/python3 ./assemble.py {shlex.quote(template)}"
    return {
        "config": {
            "concurrently": False,
            "escaping": 102,
            "script": script,
            "scriptargtype": 1,
            "scriptfile": "",
            "type": 0,
        },
        "type": "alfred.workflow.action.script",
        "uid": new_uid(),
        "version": 2,
    }


def create_clipboard_output() -> dict:
    """Copy the incoming {query} (the assembled prompt) to the clipboard."""
    return {
        "config": {
            "autopaste": False,
            "clipboardtext": "{query}",
            "ignoredynamicplaceholders": False,
            "transient": False,
        },
        "type": "alfred.workflow.output.clipboard",
        "uid": new_uid(),
        "version": 3,
    }


def create_notification(text: str) -> dict:
    return {
        "config": {
            "lastpathcomponent": False,
            "onlyshowifquerypopulated": False,
            "removeextension": False,
            "text": text,
            "title": "Feral AI",
        },
        "type": "alfred.workflow.output.notification",
        "uid": new_uid(),
        "version": 1,
    }


def create_connection(dest_uid: str) -> dict:
    return {
        "destinationuid": dest_uid,
        "modifiers": 0,
        "modifiersubtext": "",
        "vitoclose": False,
    }


def read_prompts(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_workflow(version: str) -> dict:
    prompts = read_prompts(PROMPTS_FILE)

    objects: list[dict] = []
    connections: dict[str, list[dict]] = {}
    uidata: dict[str, dict] = {}

    x_start, x_step = 90.0, 200.0
    y, y_step = 100.0, 130.0

    for prompt in prompts:
        fields = prompt["fields"]
        chain: list[dict] = []

        prior: list[str] = []
        for i, field in enumerate(fields):
            keyword = prompt["keyword"] if i == 0 else ""
            sf = create_script_filter(field, keyword, prior)
            chain.append(sf)
            prior = prior + [field["var"]]

        assemble = create_assemble_action(prompt["template"])
        clipboard = create_clipboard_output()
        notify = create_notification(
            prompt.get("notification", "Prompt copied to clipboard")
        )
        chain += [assemble, clipboard, notify]

        objects += chain

        # Wire the chain linearly: each object connects to the next.
        for a, b in zip(chain, chain[1:]):
            connections[a["uid"]] = [create_connection(b["uid"])]

        for i, obj in enumerate(chain):
            uidata[obj["uid"]] = {"xpos": x_start + i * x_step, "ypos": y}
        y += y_step

    readme = (
        "# Feral AI\n\n"
        "Alfred workflow for reusable AI prompts. Each prompt walks you through a\n"
        "guided series of fields, then copies the fully-assembled prompt to the\n"
        "clipboard.\n\n"
        "Add or edit prompts in prompts.json (+ a template file in prompts/) and\n"
        "run ./rebuild.sh to regenerate info.plist.\n\n"
        "Prompts: see prompts.json.\n"
    )

    return {
        "bundleid": "co.feralcreative.ai",
        "category": "Tools",
        "connections": connections,
        "createdby": "Ziad Ezzat",
        "description": "Guided AI prompt launcher — fills a template and copies it",
        "disabled": False,
        "name": "Feral AI",
        "objects": objects,
        "readme": readme,
        "uidata": uidata,
        "userconfigurationconfig": [],
        "variablesdontexport": [],
        "version": version,
        "webaddress": "http://feralcreative.co",
    }


def main() -> None:
    major = "--major" in sys.argv

    current = get_current_version()
    new_version = increment_version(current, major)
    print(f"Building Feral AI {current} -> {new_version}" + (" (major)" if major else ""))

    plist = build_workflow(new_version)

    with open("info.plist.new", "wb") as f:
        plistlib.dump(plist, f)

    n_sf = sum(1 for o in plist["objects"] if o["type"] == "alfred.workflow.input.scriptfilter")
    print(f"Generated info.plist.new with {len(plist['objects'])} objects "
          f"({n_sf} Script Filters across {len(read_prompts(PROMPTS_FILE))} prompt(s)).")
    print("Review info.plist.new, then rename to info.plist to activate.")


if __name__ == "__main__":
    main()
