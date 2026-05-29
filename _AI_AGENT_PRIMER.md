# AI Agent Primer - Alfred Workflows Collection

**Last Updated:** 2025-12-19  
**Repository:** <https://github.com/feralcreative/alfred.git>  
**Author:** Ziad Ezzat (<ziad@feralcreative.co>)

## 🎯 Repository Purpose

This is a **personal collection of Alfred workflows** for macOS productivity. Each workflow is self-contained in its own directory. There is **no central architecture** - each workflow is independent and can be installed/used separately.

## 📁 Repository Structure

```text
alfred/
├── README.md                    # Main documentation
├── _AI_AGENT_PRIMER.md         # This file
├── .augment/                   # AI agent rules and configuration
├── _prod/                      # Symlinks to actual Alfred directories (PRODUCTION)
│   ├── workflows/              # → Alfred.alfredpreferences/workflows
│   ├── snippets/               # → Alfred.alfredpreferences/snippets
│   ├── preferences/            # → Alfred.alfredpreferences/preferences
│   ├── resources/              # → Alfred.alfredpreferences/resources
│   └── remote/                 # → Alfred.alfredpreferences/remote
├── alfred-augment/             # Task management & process tools
├── feral-keywords/             # CSV-driven shortcuts (recently refactored)
├── feral-workspaces/           # VS Code workspace launcher
├── image-convert/              # PNG ↔ JPEG converter
├── imageoptim-ize/             # ImageOptim batch processor
├── port-roulette/              # Development port generator
└── sanitize-filenames/         # Filename sanitizer for web use
```

**IMPORTANT:** The `_prod/` directory contains symlinks to the actual Alfred preferences directory located at:
`/Volumes/Feral SSD/Dropbox (Personal)/_FERAL/_assets/settings/alfred/preferences/Alfred.alfredpreferences/`

When making changes to workflows, you must copy files to `_prod/workflows/` for Alfred to see them.

## 🔧 Technology Stack

### Core Technologies

- **Alfred 4+** with Powerpack (macOS automation platform)
- **Python 3.x** (most workflows use Python scripts)
- **AppleScript** (some workflows use AppleScript)
- **Zsh/Bash** (shell scripts for utilities)

### Python Libraries

- `plistlib` - Reading/writing Alfred workflow plists
- `Pillow` - Image processing (image-convert workflow)
- Standard library: `os`, `sys`, `json`, `pathlib`, `uuid`

### File Formats

- **`.alfredworkflow`** - Packaged workflow files (ZIP archives)
- **`info.plist`** - Alfred workflow configuration (XML property list)
- **CSV** - Configuration data (feral-keywords)
- **JSON** - Port database (port-roulette)

## 📦 Workflow Overview

### 1. alfred-augment

**Purpose:** Development productivity tools
**Keywords:** `au` (create task), `killport` (kill process on port)
**Tech:** Python, Alfred Script Filters
**Key Files:**

- `info.plist` - Workflow configuration
- `package.sh` - Packaging script
- `augment-code-tasks.alfredworkflow` - Packaged workflow

### 2. feral-keywords ⭐ (Recently Refactored)

**Purpose:** CSV-driven shortcuts for files, web URLs, and apps
**Keywords:** `scans`, `wtf`, `screenshots`, `ndr`, `www`, `cu`, `nas`, `cloud`, `sonarr`, `radarr`, `sabnzbd`, `faf`, `gclear`, `>>`
**Tech:** Python build system, CSV configuration
**Architecture:** Build-time generation (CSV → info.plist)
**Key Files:**

- `shortcuts-files.csv` - File/folder shortcuts
- `shortcuts-web.csv` - Web URL shortcuts
- `shortcuts-apps.csv` - Application shortcuts
- `build-workflow.py` - Generates info.plist from CSVs
- `rebuild.sh` - Quick rebuild script
- `utilities/gclear.sh` - Google Drive cache clearer
- `utilities/version-snippet.sh` - Version snippet generator
- `icons/` - Custom icons (auto-detected by keyword name)

**Recent Changes (2025-12-19):**

- Refactored from monolithic XML to CSV-driven system
- Added custom icon support (PNG/JPG/SVG)
- Version bumped to 2.0
- All 12 original keywords preserved for muscle memory

### 3. feral-workspaces

**Purpose:** Quick access to VS Code workspace files
**Keyword:** `dev`
**Tech:** Python Script Filter
**Key Files:**

- `info.plist` - Workflow configuration
- Workspace directory: `~/www/_vscode/workspaces/`

### 4. image-convert

**Purpose:** Convert images between PNG and JPEG
**Tech:** Python, Pillow library
**Trigger:** File action (⌥⌘\)
**Key Files:**

- `png_to_jpg.py` - Conversion script
- `requirements.txt` - Python dependencies (Pillow>=10.0.0)

### 5. imageoptim-ize

**Purpose:** Batch optimize images with ImageOptim
**Tech:** Zsh script
**Trigger:** Hotkey (ctrl+shift+cmd+I)
**Dependencies:** ImageOptim.app
**Key Files:**

- `imageOptimIze.zsh` - Main script

### 6. port-roulette

**Purpose:** Generate unique development port numbers
**Keyword:** `port`
**Tech:** Python, JSON database
**Key Files:**

- `port-roulette.py` - Main port generation logic
- `extract-port.py` - Extract port from config
- `save-port.py` - Save port to config
- Config location: `~/.config/port-roulette/ports.json`

### 7. sanitize-filenames

**Purpose:** Convert filenames to kebab-case for web use
**Tech:** AppleScript
**Trigger:** File action
**Key Files:**

- `sanitize-filenames.applescript` - Main script
- `make-a-mess.applescript` - Test file generator

## 🏗️ Alfred Workflow Architecture

### Workflow Structure

Every Alfred workflow is a directory containing:

1. **`info.plist`** (required) - XML configuration with:
   - Workflow metadata (name, version, author, description)
   - Objects (triggers, actions, filters)
   - Connections (links between objects)
   - UI data (canvas positioning)

2. **`icon.png`** (optional) - Workflow icon

3. **Scripts/executables** - Python, Bash, AppleScript, etc.

4. **Resources** - Images, data files, etc.

### Common Object Types

- `alfred.workflow.input.keyword` - Keyword trigger
- `alfred.workflow.input.scriptfilter` - Script filter (dynamic results)
- `alfred.workflow.action.script` - Run script action
- `alfred.workflow.action.openurl` - Open URL action
- `alfred.workflow.action.launchfiles` - Launch file/app action
- `alfred.workflow.output.notification` - Show notification

### Packaging Workflows

Workflows are packaged as `.alfredworkflow` files (ZIP archives with `info.plist`
at the archive root). Use the repo-level tooling — do not hand-roll `zip`:

```bash
# Build a package (delegates to package.sh under the hood)
./wf build <workflow-dir>
./wf build --all

# package.sh is the underlying engine; wf is the entrypoint you normally use
./package.sh <workflow-dir>
```

`package.sh` reads the workflow name from `info.plist`, lints it with `plutil`,
zips the whole directory flat (with a shared exclude list), and verifies the
archive. See `docs/package.md` for full details.

## 🔑 Common Patterns

### Pattern 1: CSV-Driven Configuration (feral-keywords)

```python
# Read CSV → Generate plist objects → Write info.plist
import csv, plistlib, uuid

shortcuts = list(csv.DictReader(open('shortcuts.csv')))
objects = [create_keyword_object(s) for s in shortcuts]
plistlib.dump({'objects': objects}, open('info.plist', 'wb'))
```

### Pattern 2: Script Filter Output (JSON)

```python
# Alfred expects JSON with specific structure
import json, sys

results = {
    "items": [{
        "title": "Result Title",
        "subtitle": "Description",
        "arg": "value-to-pass",
        "icon": {"path": "icon.png"}
    }]
}
print(json.dumps(results))
```

### Pattern 3: File Actions

Workflows can be triggered by selecting files in Finder:

- Alfred passes file paths as arguments
- Multiple files separated by tabs (`\t`)

### Pattern 4: Environment Variables

Alfred provides environment variables:

- `{query}` - User input
- `{var:name}` - Workflow variables
- File paths from file actions

## 🛠️ Development Workflow

### Build & Delivery (the `wf` lifecycle)

`wf` (repo root) is the single entrypoint for building and installing workflows.

```text
./wf build   [<name>|.|--all]   # package <name> into a .alfredworkflow
./wf install [<name>|.|--all]   # build, then open the package so Alfred prompts to import
./wf list                       # every workflow: name, bundle id, installed UID
./wf help
```

`<name>` is a workflow directory name (e.g. `feral-workspaces`), a path, or `.`
for the current directory. `wf build` delegates to `package.sh`; `wf install`
also runs `open` on the resulting package, which is the scripted equivalent of
double-clicking it — Alfred shows its import/update dialog for you to confirm.
With `--all`, Alfred queues one import prompt per workflow.

### Source vs. installed — why editing alone does nothing

Editing a file in a workflow's **source** directory (e.g. `feral-keywords/`) has
no effect on the running workflow. Alfred runs from its **installed** copy under
`_prod/workflows/user.workflow.<UID>/` (a symlink into the Dropbox/Feral-SSD
Alfred preferences). Alfred matches an imported workflow to its installed copy by
**bundle id** and updates it in place. So a change is only live after you
repackage **and** re-import. `wf install` does both. (`./wf list` shows the
bundle-id → installed-UID mapping.)

### Adding a New Workflow

1. Create a directory in the repository root with an `info.plist`.
2. Build the workflow in Alfred Preferences (or generate the plist with a script).
3. Add a `README.md` with documentation.
4. `./wf install <dir>` and confirm the import in Alfred.
5. Update the main `README.md`.

### Modifying Existing Workflows

1. Edit files in the workflow directory (CSV/plist/scripts).
   - For CSV-driven workflows (feral-keywords, feral-time), edit the CSVs and run
     that workflow's `build.sh` / `rebuild.sh` — it regenerates `info.plist` and
     then hands off to `wf install` automatically.
   - For others, edit the source directly.
2. `./wf install <name>` → confirm the import/update dialog in Alfred.
3. Test in Alfred, then update documentation.

### Testing Workflows

- **Alfred Debugger:** Alfred Preferences → Workflows → Click workflow → Debugger icon
- **Console Logs:** Use `print()` in Python (shows in debugger)
- **Notifications:** Use Alfred's notification action for feedback

## 📝 feral-keywords Deep Dive

This workflow was recently refactored (2025-12-19) and serves as a good example of the repository's evolution.

### Before Refactoring

- All shortcuts hardcoded in 902-line XML plist
- Difficult to add/modify shortcuts
- No clear organization

### After Refactoring

- CSV files for configuration
- Python build script generates plist
- Custom icon support
- Easy to maintain and extend

### Build Process

```bash
# 1. Edit CSV files
echo "github,GitHub,https://github.com,GitHub homepage" >> shortcuts-web.csv

# 2. Rebuild + install (regenerates info.plist, then hands off to wf install)
./build.sh            # prompts before replacing info.plist; --major for a major bump

# 3. Confirm the import/update dialog in Alfred
```

### Icon System

Icons are auto-detected from `icons/` directory:

- `icons/{keyword}.png` (or .jpg, .jpeg, .svg)
- Example: `icons/github.png` for `github` keyword
- Falls back to default icons if not found

## 🚫 What NOT to Do

1. **Don't edit `.alfredworkflow` files directly** - They're ZIP archives, extract first
2. **Don't manually edit `info.plist` for feral-keywords** - Use CSV files and rebuild
3. **Don't commit sensitive data** - No API keys, passwords, or personal paths
4. **Don't change keywords in feral-keywords** - User relies on muscle memory
5. **Don't deploy or commit without permission** - See `.augment/rules/VIOLATIONS.md`

## 🐛 Known Issues & Quirks

### feral-keywords

- Must run `rebuild.sh` after CSV changes
- Icons must be in `icons/` directory with exact keyword name
- Utilities (`gclear`, `>>`) are hardcoded in build script

### port-roulette

- Config file location: `~/.config/port-roulette/ports.json`
- Ports only saved when result is selected (not while typing)

### image-convert

- Requires Pillow library: `pip3 install Pillow`
- JPEG quality hardcoded to 90%

### imageoptim-ize

- Requires ImageOptim.app to be installed
- No progress feedback during optimization

## 📚 Key Documentation Files

- `README.md` - Main repository overview
- `feral-keywords/README.md` - Complete CSV workflow guide
- `feral-keywords/QUICK_START.md` - TL;DR for feral-keywords
- `feral-keywords/REFACTORING_PLAN.md` - Refactoring details
- `alfred-augment/PACKAGING.md` - Workflow packaging guide
- `.augment/rules/augment-rules.md` - AI agent rules
- `.augment/rules/VIOLATIONS.md` - Past mistakes to avoid

## 🎓 Learning Resources

### Alfred Workflow Development

- Alfred Preferences → Workflows → [+] → Templates
- Alfred Forum: <https://www.alfredforum.com/>
- Workflow objects documentation in Alfred

### Python for Alfred

- Use `#!/usr/bin/env python3` shebang
- Output JSON for script filters
- Use `sys.argv` for arguments
- Print to stdout for Alfred to capture

### Plist Manipulation

```python
import plistlib

# Read
with open('info.plist', 'rb') as f:
    plist = plistlib.load(f)

# Modify
plist['version'] = '2.0'

# Write
with open('info.plist', 'wb') as f:
    plistlib.dump(plist, f)
```

## 🔄 Recent Changes

### 2025-12-19

- **feral-keywords:** Complete refactoring to CSV-driven system
- **feral-keywords:** Added custom icon support (PNG/JPG/SVG)
- **feral-keywords:** Version 2.0 released
- **feral-keywords:** Added `radarr` and `sabnzbd` web shortcuts
- **Repository:** Created this AI Agent Primer
- **Repository:** Disabled CSV linting in VS Code

## 🎯 Quick Start for AI Agents

1. **Read this file first** - You're doing it!
2. **Check workflow-specific README** - Each workflow has detailed docs
3. **For feral-keywords changes:**
   - Edit CSV files in `feral-keywords/`
   - Run `./rebuild.sh`
   - Test in Alfred
4. **For other workflows:**
   - Edit scripts directly
   - Test in Alfred Debugger
   - Re-export if needed
5. **Always ask before:**
   - Committing to git
   - Deploying anything
   - Changing feral-keywords keywords
   - Installing dependencies

## 📞 Contact

**Author:** Ziad Ezzat
**Email:** <ziad@feralcreative.co>
**Website:** <http://feralcreative.co>

---

**Success Criteria:** An AI agent should be able to:

1. ✅ Understand the repository structure
2. ✅ Modify existing workflows safely
3. ✅ Add new shortcuts to feral-keywords
4. ✅ Package workflows for distribution
5. ✅ Debug issues using Alfred's tools
6. ✅ Follow the established patterns and conventions
