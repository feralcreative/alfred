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

# Clean up old package
if [ -f "Feral Workspaces.alfredworkflow" ]; then
    rm "Feral Workspaces.alfredworkflow"
    echo "🗑️  Removed old workflow package"
fi

# Package the workflow
echo "📦 Packaging workflow..."
zip -r "Feral Workspaces.alfredworkflow" info.plist icon.png *.png

# Verify package was created
if [ -f "Feral Workspaces.alfredworkflow" ]; then
    echo "✅ Workflow packaged successfully!"
    echo
    
    # Open the workflow in Alfred
    echo "🚀 Opening workflow in Alfred..."
    sleep 1  # Brief pause to ensure packaging is complete
    open "Feral Workspaces.alfredworkflow"
    echo "✅ Workflow should now be loaded in Alfred!"
else
    echo "❌ Failed to create workflow package!"
    exit 1
fi
