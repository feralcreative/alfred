#!/bin/bash
# Build script for Feral Workspaces workflow
# Usage: ./build.sh [--major]
#   Default: Increments version by 0.01 (e.g., 1.0 -> 1.01)
#   --major: Rounds up to next tenth (e.g., 1.23 -> 1.3, 1.0 -> 1.1)

set -e

# Parse command line arguments
MAJOR_UPDATE=false
if [[ "$1" == "--major" ]]; then
    MAJOR_UPDATE=true
    echo "🚀 Major update mode enabled"
fi

echo "🔨 Building Feral Workspaces workflow..."
echo

# Update version using Python script
echo "📈 Updating version..."
if [ "$MAJOR_UPDATE" = true ]; then
    python3 update-version.py --major
else
    python3 update-version.py
fi

if [ $? -ne 0 ]; then
    echo "❌ Version update failed!"
    exit 1
fi
echo

# Package + install via the repo-level wf dispatcher.
# wf builds the .alfredworkflow (using package.sh, which zips the whole dir so
# README.md and every resource are included) then opens it so Alfred prompts to
# import — confirm the dialog in Alfred.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
"$REPO/wf" install feral-workspaces
