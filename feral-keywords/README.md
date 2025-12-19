# Feral Keywords - CSV-Driven Alfred Workflow

A refactored, maintainable version of the Feral Keywords workflow. All shortcuts are now defined in simple CSV files instead of buried in XML plist files.

## Quick Start

### Adding a New Shortcut

1. **For file/folder shortcuts**: Edit `shortcuts-files.csv`
2. **For web shortcuts**: Edit `shortcuts-web.csv`
3. **For app shortcuts**: Edit `shortcuts-apps.csv`
4. Run `python3 build-workflow.py`
5. Review `info.plist.new`
6. Rename `info.plist.new` to `info.plist`
7. Reload workflow in Alfred

### Example: Adding a New File Shortcut

Open `shortcuts-files.csv` and add a line:

```csv
docs,Documents,~/Documents,My documents folder
```

That's it! Run the build script and you have a new `docs` keyword.

## CSV File Format

### shortcuts-files.csv

```csv
keyword,name,path,description
scans,Scans,/Volumes/Feral SSD/Dropbox (Personal)/_Personal/_scans,Personal document scans
```

- **keyword**: The Alfred keyword to trigger (e.g., `scans`)
- **name**: Display name shown in Alfred
- **path**: Full path to file or folder (supports `~` for home directory)
- **description**: Subtitle shown in Alfred

### shortcuts-web.csv

```csv
keyword,name,url,description
cu,Open Clickup Dashboard,https://app.clickup.com/...,ClickUp project management
```

- **keyword**: The Alfred keyword to trigger (e.g., `cu`)
- **name**: Display name shown in Alfred
- **url**: Full URL to open
- **description**: Subtitle shown in Alfred

### shortcuts-apps.csv

```csv
keyword,name,path,description
faf,Find any File,/Applications/Find Any File.app,Find Any File application
```

- **keyword**: The Alfred keyword to trigger (e.g., `faf`)
- **name**: Display name shown in Alfred
- **path**: Full path to application
- **description**: Subtitle shown in Alfred

## Custom Icons

Add custom icons for any keyword by placing an icon file in the `icons/` folder:

```text
icons/{keyword}.png   (or .jpg, .jpeg, .svg)
```

**Example:**

```bash
# Add a custom icon for the 'cu' keyword
cp ~/Downloads/clickup-icon.png icons/cu.png
./rebuild.sh
```

Supported formats: PNG, JPG, JPEG, SVG

See `icons/README.md` for details.

## Utilities

Complex utilities with custom logic are stored in `utilities/` and hardcoded in the build script:

- **gclear**: Clear Google Drive cache (`utilities/gclear.sh`)
- **>>**: Version snippet generator (`utilities/version-snippet.sh`)

To modify these, edit the shell scripts and rebuild.

## Current Shortcuts

### File/Folder Shortcuts

- `scans` - Personal document scans
- `wtf` - Dankest maymays folder
- `screenshots` - Screenshots folder
- `ndr` - Ned Davis charts
- `www` - Development projects directory

### Web Shortcuts

- `cu` - ClickUp dashboard
- `nas` - NAS web interface
- `cloud` - Cloudflare dashboard
- `sonarr` - Sonarr media management

### App Shortcuts

- `faf` - Find Any File application

### Utilities

- `gclear` - Clear Google Drive cache
- `>>` - Version snippet generator (e.g., `>> 43` → `// v00.43 - 2025.12.19.1430`)

## Build Process

The `build-workflow.py` script:

1. Reads all CSV files
2. Generates Alfred workflow objects for each shortcut
3. Creates connections between triggers and actions
4. Positions objects in the workflow canvas
5. Writes `info.plist.new`

## Benefits

✅ **Easy to Edit**: CSV files are simple text - no XML knowledge needed
✅ **Easy to Understand**: Clear column headers, one row per shortcut
✅ **Version Control**: Git diffs show exactly what changed
✅ **Easy to Add**: Just add a new row and rebuild
✅ **Documented**: Description column built into each shortcut
✅ **Portable**: Easy to backup, share, or migrate
✅ **Scalable**: Add hundreds of shortcuts without complexity

## Workflow Structure

```text
feral-keywords/
├── shortcuts-files.csv      # File/folder shortcuts
├── shortcuts-web.csv        # Web URL shortcuts
├── shortcuts-apps.csv       # Application shortcuts
├── utilities/               # Complex utility scripts
│   ├── gclear.sh           # Google Drive cache clearer
│   └── version-snippet.sh  # Version snippet generator
├── build-workflow.py        # Build script (generates info.plist)
├── info.plist              # Active workflow (generated)
├── info.plist.new          # Preview before activating
└── README.md               # This file
```

## Migration Notes

This refactored workflow maintains **100% compatibility** with the original:

- All keywords work exactly the same
- Same muscle memory
- Same functionality
- Just easier to maintain and extend

## Troubleshooting

**Q: I added a shortcut but it's not working**
A: Did you run `build-workflow.py` and rename `info.plist.new` to `info.plist`?

**Q: Can I edit info.plist directly?**
A: No! Your changes will be overwritten next time you build. Edit the CSV files instead.

**Q: How do I remove a shortcut?**
A: Delete the row from the CSV file and rebuild.

**Q: Can I change the keyword for an existing shortcut?**
A: Yes! Just edit the keyword column in the CSV and rebuild.
