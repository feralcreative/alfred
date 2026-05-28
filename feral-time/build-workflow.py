#!/usr/bin/env python3
"""Build the Feral Time Alfred workflow from shortcuts.csv.

For each row, generates three plist objects (snippet trigger -> script -> paste)
plus the two connections that wire them together, then writes info.plist.new.
"""

import csv
import os
import plistlib
import re
import shlex
import uuid

CSV_FILE = "shortcuts.csv"
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


def create_snippet_trigger(trigger: str) -> dict:
    """Snippet trigger that fires when the user types `trigger` text inline.

    Field name is `keyword` (verified against Alfred 5 by inspecting a
    trigger created via the Alfred Preferences UI). The `focusedapp*` pair
    gates the trigger by frontmost app — both empty/false = fire globally.
    """
    return {
        "config": {
            "focusedappvariable": False,
            "focusedappvariablename": "",
            "keyword": trigger,
        },
        "type": "alfred.workflow.trigger.snippet",
        "uid": new_uid(),
        "version": 1,
    }


def create_script_action(tz: str, fmt: str) -> dict:
    """Run time-snippet.py with the given args. Script type 0 = /bin/bash."""
    script = f"/usr/bin/python3 ./time-snippet.py {shlex.quote(tz)} {shlex.quote(fmt)}"
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


def create_paste_action() -> dict:
    """Cmd+V into front-most app — same params as feral-keywords' >> paste."""
    return {
        "config": {
            "count": 1,
            "keychar": "v",
            "keycode": -1,
            "keymod": 1048576,
            "overridewithargument": False,
        },
        "type": "alfred.workflow.output.dispatchkeycombo",
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


def read_shortcuts(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_workflow(version: str) -> dict:
    shortcuts = read_shortcuts(CSV_FILE)

    objects: list[dict] = []
    connections: dict[str, list[dict]] = {}
    uidata: dict[str, dict] = {}

    x_trigger, x_script, x_paste = 90.0, 290.0, 490.0
    y, y_step = 100.0, 110.0

    for row in shortcuts:
        trigger = row["trigger"]
        tz = row["tz"]
        fmt = row["format"]
        subtext = row.get("subtext", "")

        snip = create_snippet_trigger(trigger)
        script = create_script_action(tz, fmt)
        paste = create_paste_action()

        objects += [snip, script, paste]

        connections[snip["uid"]] = [create_connection(script["uid"])]
        connections[script["uid"]] = [create_connection(paste["uid"])]

        uidata[snip["uid"]] = {"xpos": x_trigger, "ypos": y, "note": subtext}
        uidata[script["uid"]] = {"xpos": x_script, "ypos": y}
        uidata[paste["uid"]] = {"xpos": x_paste, "ypos": y}
        y += y_step

    readme = """# Feral Time

Snippet-trigger Alfred workflow for date/time insertion across timezones.
Edit shortcuts.csv and run ./rebuild.sh to regenerate info.plist.

Triggers: see shortcuts.csv. Local-time originals + UTC/Hawaii/Pacific/
Mountain/Central/Eastern variants.
"""

    return {
        "bundleid": "co.feralcreative.time",
        "category": "Tools",
        "connections": connections,
        "createdby": "Ziad Ezzat",
        "description": "Timezone-aware date/time snippet triggers",
        "disabled": False,
        "name": "Feral Time",
        "objects": objects,
        "readme": readme,
        "uidata": uidata,
        "userconfigurationconfig": [],
        "variablesdontexport": [],
        "version": version,
        "webaddress": "http://feralcreative.co",
    }


def main() -> None:
    import sys

    major = "--major" in sys.argv

    current = get_current_version()
    new_version = increment_version(current, major)
    print(f"Building Feral Time {current} -> {new_version}" + (" (major)" if major else ""))

    plist = build_workflow(new_version)

    with open("info.plist.new", "wb") as f:
        plistlib.dump(plist, f)

    n_triggers = sum(1 for o in plist["objects"] if o["type"] == "alfred.workflow.trigger.snippet")
    print(f"Generated info.plist.new with {len(plist['objects'])} objects "
          f"({n_triggers} snippet triggers).")
    print("Review info.plist.new, then rename to info.plist to activate.")


if __name__ == "__main__":
    main()
