# Feral Keywords - Quick Start Guide

## TL;DR

Your Alfred workflow is now CSV-driven. Edit CSV files instead of XML.

## Adding a New Shortcut

### 1. Edit the CSV file

**For a file/folder:**
```bash
# Edit shortcuts-files.csv
docs,Documents,~/Documents,My documents folder
```

**For a website:**
```bash
# Edit shortcuts-web.csv
github,GitHub,https://github.com,GitHub homepage
```

**For an app:**
```bash
# Edit shortcuts-apps.csv
vscode,VS Code,/Applications/Visual Studio Code.app,VS Code editor
```

### 2. Rebuild the workflow

```bash
./rebuild.sh
```

Or manually:
```bash
python3 build-workflow.py
mv info.plist.new info.plist
```

### 3. Reload in Alfred

Open Alfred Preferences → Workflows → Right-click "Feral Keywords" → Reload Workflow

## That's It!

Your new keyword now works exactly like the old ones.

## CSV Format

```csv
keyword,name,path_or_url,description
```

- **keyword**: What you type in Alfred (e.g., `docs`)
- **name**: Display name in Alfred
- **path_or_url**: Where to go (file path or URL)
- **description**: Subtitle shown in Alfred

## Examples

```csv
# File shortcuts
downloads,Downloads,~/Downloads,Downloads folder
desktop,Desktop,~/Desktop,Desktop folder

# Web shortcuts
gmail,Gmail,https://mail.google.com,Gmail inbox
calendar,Calendar,https://calendar.google.com,Google Calendar

# App shortcuts
chrome,Chrome,/Applications/Google Chrome.app,Chrome browser
```

## Current Keywords

- `scans`, `wtf`, `screenshots`, `ndr`, `www` - Files/folders
- `cu`, `nas`, `cloud`, `sonarr` - Websites
- `faf` - Applications
- `gclear` - Clear Google Drive cache
- `>>` - Version snippet generator

## Need Help?

See `README.md` for full documentation.

