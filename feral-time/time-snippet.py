#!/usr/bin/env python3
"""Format the current date/time for a given timezone and strftime format.

Usage: time-snippet.py <tz> <strftime_format>
  <tz>: IANA zone name (e.g. "UTC", "America/Los_Angeles") or "local"
  <strftime_format>: e.g. "%y%m%dT%H%MZ"

Writes the formatted string to stdout (no trailing newline) and copies to
clipboard via pbcopy so the downstream Cmd+V paste action has the value.
"""

import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def main() -> None:
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: time-snippet.py <tz> <strftime_format>\n")
        sys.exit(1)

    tz_name, fmt = sys.argv[1], sys.argv[2]
    now = datetime.now() if tz_name == "local" else datetime.now(ZoneInfo(tz_name))
    out = now.strftime(fmt)

    subprocess.run(["pbcopy"], input=out.encode("utf-8"), check=False)
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
