#!/bin/bash

# Package the Port Roulette Alfred Workflow

# Create a temporary directory for packaging
TEMP_DIR=$(mktemp -d)
WORKFLOW_NAME="port-roulette.alfredworkflow"

echo "Packaging Port Roulette Alfred Workflow..."

# Copy necessary files to temp directory
cp port-roulette.py "$TEMP_DIR/"
cp info.plist "$TEMP_DIR/"
cp icon.png "$TEMP_DIR/"

# Create the workflow package
cd "$TEMP_DIR"
zip -r "../$WORKFLOW_NAME" .

# Move the workflow file to the current directory
mv "../$WORKFLOW_NAME" "$OLDPWD/"

# Clean up
rm -rf "$TEMP_DIR"

echo "Created $WORKFLOW_NAME"
echo "Double-click to install in Alfred"