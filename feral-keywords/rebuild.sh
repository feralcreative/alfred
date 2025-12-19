#!/bin/bash
# Quick rebuild script for Feral Keywords workflow
# Run this after editing CSV files

set -e

echo "🔨 Rebuilding Feral Keywords workflow..."
echo

# Build the workflow
python3 build-workflow.py

# Check if build was successful
if [ -f "info.plist.new" ]; then
    echo
    echo "✅ Build successful!"
    echo
    read -p "Replace info.plist with the new version? [Y/n] " -n 1 -r
    echo

    # Default to Yes if user just presses Enter (empty response)
    if [[ -z $REPLY ]] || [[ $REPLY =~ ^[Yy]$ ]]; then
        # Backup current plist
        cp info.plist info.plist.backup
        # Replace with new version
        mv info.plist.new info.plist
        echo "✅ Workflow updated! Reload in Alfred to see changes."
        echo

        # Package the workflow
        echo "📦 Packaging workflow..."
        ./package.sh
    else
        echo "ℹ️  New workflow saved as info.plist.new"
        echo "   Review it and manually rename when ready."
    fi
else
    echo "❌ Build failed!"
    exit 1
fi
