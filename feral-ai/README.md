# Feral AI

Alfred workflow for reusable AI prompts. Each prompt walks you through a guided
series of fields — one at a time — then copies the fully-assembled prompt to the
clipboard, ready to paste into an AI chat.

## Prompts

### `air` — Company Research (MCP)

Kicks off a fully-cited client research task that populates the `cb-client-mcp`
knowledge base (per `~/.claude/docs/COMPANY_RESEARCH_INSTRUCTIONS.md`). Alfred
prompts for four fields in sequence:

1. **Company name** (required) — exact legal / trade name.
2. **Exchange** (optional) — leave blank for a private company.
3. **Ticker** (optional) — leave blank for a private company.
4. **Client slug** (required) — lowercase output directory name.

If exchange and ticker are both left blank, the prompt renders `(private)`;
otherwise it renders `(EXCHANGE: TICKER)`. The assembled prompt is copied to the
clipboard and a notification confirms it.

## How it works

Each prompt is a chain of Alfred Script Filters — one per field — ending in a
Run Script, a Clipboard output, and a Notification:

```text
[air] SF:COMPANY → SF:EXCHANGE → SF:TICKER → SF:SLUG → assemble → clipboard → notify
```

Actioning a field's item sets its own workflow variable; Alfred carries prior
variables forward automatically. The final `assemble.py` reads all collected
variables from the environment, substitutes them into the template, and prints
the result, which the Clipboard output copies.

## Files

```text
feral-ai/
├── prompts.json              # prompt definitions (keyword, fields, template path)
├── prompts/
│   └── company-research.txt  # template body with {{COMPANY}} {{EXCHANGE_TICKER}} {{SLUG}}
├── prompt-field.py           # generic per-field Script Filter (runtime)
├── assemble.py               # generic template assembler (runtime)
├── build-workflow.py         # generates info.plist from prompts.json
├── rebuild.sh                # version bump → build → wf install
├── info.plist                # generated — do not edit by hand
└── README.md
```

## Adding a prompt

1. Add a template file under `prompts/`, using `{{TOKEN}}` placeholders. Tokens
   map to environment variables of the same name; `{{EXCHANGE_TICKER}}` is a
   computed convenience token (`EXCHANGE: TICKER`, or `private` when both are
   blank).
2. Add an entry to `prompts.json` with a unique `keyword`, a `template` path, an
   optional `notification`, and the ordered `fields` (each with `var`, `label`,
   `hint`, and `required`).
3. Run `./rebuild.sh` (or `./rebuild.sh --major`) and confirm the import dialog
   in Alfred.

## Build

```bash
./rebuild.sh            # minor version bump, build, install
./rebuild.sh --major    # major version bump
```

`rebuild.sh` regenerates `info.plist`, lints it with `plutil`, then hands off to
the repo-level `wf install` to package and open it for Alfred to import.
