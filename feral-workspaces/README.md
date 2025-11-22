# Feral Workspaces

An Alfred workflow for quickly opening VS Code workspace files from your development directory.

## Overview

**Feral Workspaces** is a productivity-focused Alfred workflow that provides instant access to your VS Code workspace files. Instead of manually navigating through folders or using VS Code's recent files, simply type `dev` in Alfred and start typing your project name to quickly open any workspace.

## Features

- 🚀 **Fast Fuzzy Search**: Type partial project names to find workspaces instantly
- 🎯 **Smart Filtering**: Automatically excludes system files (`.DS_Store`, `.localized`, etc.)
- 🎨 **Custom Icons**: Supports project-specific icons for visual identification
- 📁 **Organized Structure**: Scans your dedicated workspace directory
- ⚡ **Direct Integration**: Opens workspaces directly in VS Code

## Installation

1. Download the `Feral Workspaces.alfredworkflow` file
2. Double-click to install in Alfred
3. Ensure your workspace files are located in `~/www/_vscode/workspaces/`

## Usage

1. **Activate Alfred** (default: `⌘ + Space`)
2. **Type `dev`** followed by your project name
3. **Select workspace** from the filtered results
4. **Press Enter** to open in VS Code

### Example
```
dev myproject    → Shows "myproject.code-workspace"
dev web         → Shows all workspaces containing "web"
dev             → Shows all available workspaces
```

## Directory Structure

The workflow expects your workspace files to be organized as follows:

```
~/www/_vscode/workspaces/
├── project1.code-workspace
├── project2.code-workspace
├── webapp.code-workspace
└── icons/
    ├── icon-project1.png
    ├── icon-project2.png
    └── icon-webapp.png
```

## Custom Icons

To add custom icons for your workspaces:

1. Create an `icons` folder in your workspaces directory
2. Add PNG files named `icon-{projectname}.png`
3. Use lowercase names with spaces removed (e.g., "My Project" → `icon-myproject.png`)

If no custom icon exists, the workflow uses the default icon.

## Configuration

- **Keyword**: `dev` (can be changed in Alfred preferences)
- **Workspace Directory**: `~/www/_vscode/workspaces/` (hardcoded)
- **Supported Files**: `.code-workspace` files only

## Technical Details

- **Version**: 1.0
- **Author**: Ziad Ezzat (@feralcreative)
- **Bundle ID**: `dev.feralcreative.workspace`
- **Alfred Version**: Compatible with Alfred 5+

## Workflow Components

1. **Script Filter**: Python script that scans workspace directory and provides fuzzy matching
2. **Open File Action**: Opens selected workspace file in VS Code

## Troubleshooting

### No workspaces found
- Ensure workspace files are in `~/www/_vscode/workspaces/`
- Check that files have `.code-workspace` extension
- Verify directory permissions

### Icons not showing
- Check icon files are in `~/www/_vscode/workspaces/icons/`
- Ensure icon names match pattern: `icon-{projectname}.png`
- Use lowercase names without spaces

### Workflow not responding
- Check Alfred permissions for the workflow
- Verify Python 3 is available at `/usr/bin/env python3`

## Development

The workflow is built with:
- Python 3 for the script filter logic
- Alfred's built-in file opening action
- Custom fuzzy matching algorithm

## License

Created by Ziad Ezzat for Feral Creative. Visit [feralcreative.dev](https://feralcreative.dev) for more tools and workflows.
