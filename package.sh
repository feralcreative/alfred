#!/bin/bash

# Alfred Workflow Packager
# This script packages the Alfred workflow files into a .alfredworkflow file

set -e  # Exit on any error

# Configuration
WORKFLOW_NAME="augment-code-tasks"
REQUIRED_FILES=("info.plist")
OPTIONAL_FILES=("icon.png" "README.md")

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

# Function to check if required files exist
check_required_files() {
    print_status "Checking required files..."
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [[ ! -f "$file" ]]; then
            print_error "Required file '$file' not found!"
            exit 1
        fi
        print_status "✓ Found required file: $file"
    done
}

# Function to validate plist file
validate_plist() {
    print_status "Validating info.plist..."
    
    if command -v plutil >/dev/null 2>&1; then
        if plutil -lint info.plist >/dev/null 2>&1; then
            print_success "✓ info.plist is valid"
        else
            print_error "info.plist validation failed!"
            plutil -lint info.plist
            exit 1
        fi
    else
        print_warning "plutil not found, skipping plist validation"
    fi
}

# Function to collect files to package
collect_files() {
    local files_to_package=()
    
    # Add required files
    for file in "${REQUIRED_FILES[@]}"; do
        files_to_package+=("$file")
    done
    
    # Add optional files if they exist
    for file in "${OPTIONAL_FILES[@]}"; do
        if [[ -f "$file" ]]; then
            files_to_package+=("$file")
            print_status "✓ Including optional file: $file"
        else
            print_warning "Optional file '$file' not found, skipping"
        fi
    done
    
    echo "${files_to_package[@]}"
}

# Function to create the workflow package
create_package() {
    local files_to_package=($1)
    local workflow_file="${WORKFLOW_NAME}.alfredworkflow"
    
    print_status "Creating workflow package: $workflow_file"
    
    # Remove existing workflow file if it exists
    if [[ -f "$workflow_file" ]]; then
        rm "$workflow_file"
        print_status "Removed existing workflow file"
    fi
    
    # Create the zip file
    if zip -r "$workflow_file" "${files_to_package[@]}" >/dev/null 2>&1; then
        print_success "✓ Created workflow package: $workflow_file"
    else
        print_error "Failed to create workflow package!"
        exit 1
    fi
    
    # Verify the package
    if unzip -t "$workflow_file" >/dev/null 2>&1; then
        print_success "✓ Workflow package verified successfully"
    else
        print_error "Workflow package verification failed!"
        exit 1
    fi
}

# Function to show package info
show_package_info() {
    local workflow_file="${WORKFLOW_NAME}.alfredworkflow"
    local file_size=$(ls -lh "$workflow_file" | awk '{print $5}')
    
    print_success "Package created successfully!"
    echo
    echo "📦 Workflow Details:"
    echo "   File: $workflow_file"
    echo "   Size: $file_size"
    echo
    echo "📋 Contents:"
    unzip -l "$workflow_file" | grep -E "^\s+[0-9]+" | awk '{print "   " $4 " (" $1 " bytes)"}'
    echo
    echo "🚀 Ready to install in Alfred!"
    echo "   Double-click the .alfredworkflow file to install"
}

# Main execution
main() {
    echo "🔧 Alfred Workflow Packager"
    echo "================================"
    echo
    
    # Check if we're in the right directory
    if [[ ! -f "info.plist" ]]; then
        print_error "info.plist not found. Are you in the workflow directory?"
        exit 1
    fi
    
    # Run the packaging process
    check_required_files
    validate_plist
    
    local files_to_package=$(collect_files)
    create_package "$files_to_package"
    
    show_package_info
}

# Run the script
main "$@"
