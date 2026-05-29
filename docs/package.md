# package.sh

Generic packager that turns an Alfred workflow source directory into an
installable `.alfredworkflow` file. It lives at the repo root and is the single
canonical packaging path for every workflow in this collection.

## What it does

A `.alfredworkflow` file is just a ZIP archive of a workflow's files with
`info.plist` at the archive root. `package.sh` builds that archive for you:

1. Validates that the target directory has an `info.plist`.
2. Lints the `info.plist` with `plutil` (skipped if `plutil` is unavailable).
3. Reads the workflow's display name from the `name` key in `info.plist`.
4. Zips the directory contents flat (no wrapping folder), excluding build
   artifacts and cruft.
5. Verifies the resulting archive with `unzip -t`.
6. Writes `<Workflow Name>.alfredworkflow` alongside the source `info.plist`.

The output filename always matches the plist `name` key exactly, so repackaging
overwrites the previous artifact rather than creating a differently named
duplicate.

## Usage

```bash
./package.sh                 # package the workflow in the current directory
./package.sh <workflow-dir>  # package a specific workflow directory
./package.sh --all           # package every workflow directory in the repo
./package.sh --help          # print usage
```

### Examples

```bash
# From the repo root, package one workflow
./package.sh feral-workspaces

# From inside a workflow directory
cd feral-keywords && ../package.sh

# Rebuild every workflow at once
./package.sh --all
```

## Behavior details

### Name resolution

The workflow name comes from the `name` key in `info.plist`. The script reads it
with `plutil -extract name raw` when `plutil` is present, and falls back to an
`awk` scrape of the `<key>name</key>` value otherwise. If the name cannot be
read, the workflow is skipped with an error.

### Excluded files

These patterns are excluded from every package so stale and local-only files
never ship inside a workflow:

```text
*.backup  *.bak  *.new  *.old
*.sync-conflict-*
*.pyc  __pycache__/  __pycache__
.DS_Store  */.DS_Store
.git/  .git
*.alfredworkflow
```

The `*.alfredworkflow` exclusion prevents a previously built package from being
nested inside a new one.

### Flat archive layout

Packaging runs `zip -r` from **inside** the workflow directory, so `info.plist`,
`icon.png`, scripts, and resource folders all sit at the archive root. This is
the layout Alfred expects when importing a workflow.

### `--all` behavior

`--all` iterates over every immediate subdirectory of the repo root, **skipping**
any directory whose name begins with an underscore (for example `_prod`). A
directory without an `info.plist` at its root is skipped with a warning rather
than treated as an error, so non-workflow folders such as `docs/` are ignored.

## Exit status

- Returns `0` when packaging succeeds.
- `package_one` returns non-zero for a missing `info.plist`, a failed `plutil`
  lint, an unreadable workflow name, or a failed archive verification.
- With `--all`, the run continues past a failing workflow and the overall exit
  status is non-zero if any single workflow failed.

## Requirements

- `bash`, `zip`, and `unzip` (all standard on macOS).
- `plutil` (ships with macOS) for plist linting and fast name extraction. The
  script degrades gracefully without it, skipping the lint and using the `awk`
  fallback for the name.

## Relationship to `wf` and installing

`package.sh` only **builds** the `.alfredworkflow` artifact; it does not install
anything in Alfred. To make a change live, the package must be imported into
Alfred (Alfred matches by bundle id and updates the installed copy in place).

The repo-level `wf` dispatcher wraps this script and adds the install step:

- `wf build <name>` delegates to `package.sh`.
- `wf install <name>` builds, then opens the package so Alfred shows its import
  dialog.

See `_AI_AGENT_PRIMER.md` for the full edit → build → install lifecycle.
