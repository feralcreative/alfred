#!/bin/bash
# Build script for Feral Keywords workflow
# Usage: ./build.sh [--major]
#   Default: Increments version by 0.01 (e.g., 2.0 -> 2.01)
#   --major: Rounds up to next tenth (e.g., 2.23 -> 2.3, 2.0 -> 2.1)
# Run this after editing CSV files

set -e

echo "🔨 Building Feral Keywords workflow..."
echo

# Build the workflow (Python script handles version increment)
if [[ "$1" == "--major" ]]; then
    echo "🚀 Major update mode enabled"
    python3 build-workflow.py --major
else
    python3 build-workflow.py
fi

# Check if build was successful
if [ -f "info.plist.new" ]; then
    echo
    echo "📋 Replace info.plist with the new version? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        mv info.plist.new info.plist
        echo "✅ info.plist updated!"
        
        # Package the workflow
        echo
        echo "📦 Packaging workflow..."
        ./package.sh
        
        # Open the workflow in Alfred
        if [ -f "Feral Keywords.alfredworkflow" ]; then
            echo "🚀 Opening workflow in Alfred..."
            sleep 1  # Brief pause to ensure packaging is complete
            open "Feral Keywords.alfredworkflow"
            echo "✅ Workflow should now be loaded in Alfred!"
        fi
    else
        echo "❌ Build cancelled. Review info.plist.new manually."
        exit 1
    fi
else
    echo "❌ Build failed - no info.plist.new generated"
    exit 1
fi
