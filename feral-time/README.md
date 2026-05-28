# Feral Time

Alfred workflow that inserts the current date/time at the cursor using
snippet triggers. Supports local time and timezone-aware variants
(UTC/Zulu, Hawaii, Pacific, Mountain, Central, Eastern).

## Triggers

### Local time

| Trigger | Example output       |
| ------- | -------------------- |
| `ddt-`  | `2026-05-20-1604`    |
| `ddt.`  | `2026.05.20.1604`    |
| `ddd-`  | `2026-05-20`         |
| `ddd.`  | `2026.05.20`         |
| `ddf`   | `2026-05-20 16:04`   |

### Timezones

Each zone has three variants: compact (trigger + space), dash, and dot.
Suffix is the zone abbreviation; the underlying time uses the IANA zone
so DST is handled correctly.

| Zone     | IANA                  | Compact (+space) | Dash    | Dot     |
| -------- | --------------------- | ---------------- | ------- | ------- |
| Zulu     | `UTC`                 | `ddz `           | `ddz-`  | `ddz.`  |
| Hawaii   | `Pacific/Honolulu`    | `ddh `           | `ddh-`  | `ddh.`  |
| Pacific  | `America/Los_Angeles` | `ddp `           | `ddp-`  | `ddp.`  |
| Mountain | `America/Denver`      | `ddm `           | `ddm-`  | `ddm.`  |
| Central  | `America/Chicago`     | `ddc `           | `ddc-`  | `ddc.`  |
| Eastern  | `America/New_York`    | `dde `           | `dde-`  | `dde.`  |

Example outputs (assuming `2026-05-20 16:04` Pacific):

```text
ddz<space>  -> 260520T1604Z
ddz-        -> 2026-05-20-1604Z
ddp<space>  -> 260520T1604PT
ddp-        -> 2026-05-20-1604PT
```

## How it works

Each row in `shortcuts.csv` generates three plist objects:

1. **Snippet trigger** (`alfred.workflow.trigger.snippet`) — fires when the
   trigger text is typed; replaces the typed text.
2. **Script action** — runs `time-snippet.py <tz> <strftime_format>`.
3. **Paste action** — Cmd+V into the front-most app.

`time-snippet.py` uses Python's stdlib `zoneinfo` (Python 3.9+), so no
dependencies are required beyond system Python 3.

## Rebuilding

After editing `shortcuts.csv`:

```bash
./rebuild.sh
```

`--major` bumps to the next 0.1 version; otherwise patch-bumps 0.01.

To add a new timezone, append a row to `shortcuts.csv`:

```csv
trigger,tz,format,subtext
ddjp,Asia/Tokyo,%y%m%dT%H%MJST,Japan compact
```

## Deployment

Alfred reads workflows from `Alfred.alfredpreferences/workflows/<UID>/`.
Symlinked from the repo via `_prod/workflows/` — see the root primer for
the deploy path.

**Migration:** delete the equivalent global snippets (`ddt-`, `ddt.`,
`ddd-`, `ddd.`, `ddf`) from Alfred Preferences -> Features -> Snippets
once this workflow is installed, or both will fire.

## Verification

```bash
python3 time-snippet.py UTC '%y%m%dT%H%MZ'
python3 time-snippet.py America/Los_Angeles '%y%m%dT%H%MPT'
python3 time-snippet.py Pacific/Honolulu '%y%m%dT%H%MHT'
```
