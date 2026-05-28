#!/usr/bin/env bash
# Generic Alfred workflow packager.
#
# Usage:
#   ./package.sh                   # packages the workflow in the current dir
#   ./package.sh <workflow-dir>    # packages a specific workflow dir
#   ./package.sh --all             # packages every workflow dir in the repo
#
# Reads the workflow name from info.plist and writes
# "<Workflow Name>.alfredworkflow" alongside info.plist. The .alfredworkflow
# file is a plain zip with all workflow files at the archive root (no
# wrapping directory) — double-click to install in Alfred.

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()      { echo -e "${GREEN}[OK]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()     { echo -e "${RED}[ERR]${NC} $1" >&2; }

# Files/dirs excluded from every package.
EXCLUDES=(
  '*.backup' '*.bak' '*.new' '*.old'
  '*.sync-conflict-*'
  '*.pyc' '__pycache__/*' '__pycache__'
  '.DS_Store' '*/.DS_Store'
  '.git/*' '.git'
  '*.alfredworkflow'   # don't nest old packages
)

# Read the workflow name from info.plist. Tries plutil first (fast, ships with
# macOS), falls back to a sed/awk dance if needed.
workflow_name() {
  local plist="$1"
  if command -v plutil >/dev/null; then
    plutil -extract name raw -o - "$plist" 2>/dev/null && return
  fi
  # Fallback: grab the string after <key>name</key>
  awk '/<key>name<\/key>/{getline; gsub(/.*<string>|<\/string>.*/, ""); print; exit}' "$plist"
}

package_one() {
  local dir="$1"
  dir="${dir%/}"

  if [[ ! -f "$dir/info.plist" ]]; then
    err "$dir: no info.plist — skipping"
    return 1
  fi

  info "Packaging: $dir"

  if command -v plutil >/dev/null; then
    if ! plutil -lint "$dir/info.plist" >/dev/null; then
      err "$dir/info.plist failed lint"
      return 1
    fi
  fi

  local name
  name="$(workflow_name "$dir/info.plist")"
  if [[ -z "$name" ]]; then
    err "$dir: could not read workflow name from info.plist"
    return 1
  fi

  local outfile="$dir/${name}.alfredworkflow"
  rm -f "$outfile"

  # Build -x args for zip.
  local zip_excludes=()
  for pattern in "${EXCLUDES[@]}"; do
    zip_excludes+=(-x "$pattern")
  done

  # zip from inside the workflow dir so the archive is flat at the root.
  ( cd "$dir" && zip -r "${name}.alfredworkflow" . "${zip_excludes[@]}" >/dev/null )

  if ! unzip -t "$outfile" >/dev/null 2>&1; then
    err "$outfile: archive failed verification"
    return 1
  fi

  local size
  size="$(ls -lh "$outfile" | awk '{print $5}')"
  ok "$outfile ($size)"
}

package_all() {
  local repo_root
  repo_root="$(cd "$(dirname "$0")" && pwd)"
  local rc=0
  for d in "$repo_root"/*/; do
    [[ "$(basename "$d")" == _* ]] && continue   # skip _prod and similar
    if [[ ! -f "$d/info.plist" ]]; then
      warn "$(basename "$d"): no info.plist at dir root — skipping"
      echo
      continue
    fi
    package_one "$d" || rc=1
    echo
  done
  return "$rc"
}

main() {
  case "${1:-}" in
    -h|--help)
      sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    --all)
      package_all
      ;;
    "")
      package_one "."
      ;;
    *)
      package_one "$1"
      ;;
  esac
}

main "$@"
