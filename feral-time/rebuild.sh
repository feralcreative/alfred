#!/usr/bin/env bash
# Quick rebuild for the Feral Time workflow.
# Usage: ./rebuild.sh [--major]
set -e

cd "$(dirname "$0")"

if [[ "$1" == "--major" ]]; then
  python3 build-workflow.py --major
else
  python3 build-workflow.py
fi

if [[ ! -f info.plist.new ]]; then
  echo "Build failed: info.plist.new was not generated." >&2
  exit 1
fi

if command -v plutil >/dev/null 2>&1; then
  if ! plutil -lint info.plist.new >/dev/null; then
    echo "info.plist.new failed plutil lint; leaving it in place for inspection." >&2
    exit 1
  fi
fi

mv info.plist.new info.plist
echo "info.plist updated."

# Package + install via the repo-level wf dispatcher (cwd is already this dir).
# wf builds the .alfredworkflow (using package.sh) then opens it so Alfred
# prompts to import — confirm the dialog in Alfred.
REPO="$(cd .. && pwd)"
"$REPO/wf" install feral-time
