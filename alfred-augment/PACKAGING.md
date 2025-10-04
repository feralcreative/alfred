# Alfred Workflow Packaging

## Quick Start

To package your Alfred workflow, simply run:

```bash
./package.sh
```

## What the Script Does

The `package.sh` script automatically:

1. ✅ **Validates** your `info.plist` file for XML errors
2. 📁 **Collects** all necessary files (required + optional)
3. 📦 **Creates** the `.alfredworkflow` package
4. ✔️ **Verifies** the package integrity
5. 📊 **Shows** package details and contents

## Required Files

- `info.plist` - Main workflow configuration (required)

## Optional Files (included if present)

- `icon.png` - Workflow icon
- `README.md` - Documentation

## Output

The script creates `augment-code-tasks.alfredworkflow` ready for installation in Alfred.

## Features

- 🎨 **Colored output** for easy reading
- 🔍 **Automatic validation** of plist files
- 📋 **Detailed package information**
- ⚡ **Error handling** with clear messages
- 🔄 **Overwrites** existing packages automatically

## Usage Examples

```bash
# Basic packaging
./package.sh

# Make the script executable (if needed)
chmod +x package.sh
```

## Troubleshooting

- **"info.plist not found"**: Make sure you're in the workflow directory
- **"plist validation failed"**: Check your XML syntax in info.plist
- **"Required file not found"**: Ensure info.plist exists in the current directory

The script will show detailed error messages to help you fix any issues.
