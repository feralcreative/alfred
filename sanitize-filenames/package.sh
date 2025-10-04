#!/bin/bash

# Alfred Workflow Packager - Sanitize Filenames
# This script packages the Alfred workflow files into a .alfredworkflow file

set -e  # Exit on any error

# Configuration
WORKFLOW_NAME="sanitize-filenames"
REQUIRED_FILES=("sanitize-filenames.applescript")
OPTIONAL_FILES=("icon.png" "README.md" "LICENSE" "make-a-mess.applescript")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Header
echo -e "${BLUE}🧹 Alfred Workflow Packager${NC}"
echo "================================"
echo

# Check if required files exist
print_status "Checking required files..."
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        print_status "✓ Found required file: $file"
    else
        print_error "✗ Missing required file: $file"
        exit 1
    fi
done

# Create workflow package
WORKFLOW_FILE="${WORKFLOW_NAME}.alfredworkflow"
print_status "Creating workflow package: $WORKFLOW_FILE"

# Remove existing workflow file if it exists
if [[ -f "$WORKFLOW_FILE" ]]; then
    rm "$WORKFLOW_FILE"
    print_status "Removed existing workflow file"
fi

# Create zip file with required files
zip -q "$WORKFLOW_FILE" "${REQUIRED_FILES[@]}"

# Add optional files if they exist
for file in "${OPTIONAL_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        zip -q "$WORKFLOW_FILE" "$file"
        print_status "Added optional file: $file"
    else
        print_warning "Optional file not found: $file"
    fi
done

# Verify the package was created
if [[ -f "$WORKFLOW_FILE" ]]; then
    print_success "✓ Created workflow package: $WORKFLOW_FILE"
    
    # Test the zip file
    if zip -T "$WORKFLOW_FILE" >/dev/null 2>&1; then
        print_success "✓ Workflow package verified successfully"
    else
        print_error "✗ Workflow package verification failed"
        exit 1
    fi
    
    print_success "Package created successfully!"
    echo
    echo -e "${BLUE}📦 Workflow Details:${NC}"
    echo "   File: $WORKFLOW_FILE"
    echo "   Size: $(du -h "$WORKFLOW_FILE" | cut -f1)"
    echo
    echo -e "${BLUE}📋 Contents:${NC}"
    unzip -l "$WORKFLOW_FILE" | tail -n +4 | head -n -2 | while read -r line; do
        echo "   $line"
    done
    echo
    echo -e "${GREEN}🚀 Ready to install in Alfred!${NC}"
    echo "   Double-click the .alfredworkflow file to install"
else
    print_error "✗ Failed to create workflow package"
    exit 1
fi
