# Feral Keywords Workflow Refactoring Plan

## Current State

The `feral-keywords` workflow contains **13 shortcuts** in a single monolithic workflow:

### File/Folder Access

- `scans` → `/Volumes/Feral SSD/Dropbox (Personal)/_Personal/_scans`
- `wtf` → `/Volumes/Feral SSD/Dropbox (Personal)/wtf`
- `screenshots` → `/Volumes/Feral SSD/Dropbox (Personal)/Screenshots`
- `ndr` → `/Volumes/Feral SSD/Dropbox (Personal)/_FERAL/Westwood/assets/charts/ned-davis-charts`
- `www` → `~/www`

### Web Services

- `cu` → `https://app.clickup.com/9014243918/dashboards/8cmmwje-13934`
- `nas` → `https://nas.feralcreative.co`
- `cloud` → `https://dash.cloudflare.com/`
- `sonarr` → `http://feralcreative.synology.me:8989`

### Applications

- `faf` → `/Applications/Find Any File.app`

### Utilities

- `gclear` → Clear Google Drive cache (AppleScript)
- `>>` → Version snippet generator (shell script with date/time)
- Paste action → Cmd+V key combo

## Problems

1. **Monolithic Structure**: All shortcuts in one workflow, hard to maintain
2. **No Categorization**: Mixed purposes in one place
3. **Hard to Scale**: Adding shortcuts requires editing complex plist XML
4. **Difficult Discovery**: No way to browse available shortcuts
5. **No Documentation**: Shortcuts only documented in plist

## Constraints

- **MUST keep existing keywords** - muscle memory is critical
- **MUST maintain ease of editing** - should be simpler than current plist editing
- **MUST maintain ease of understanding** - clear what each shortcut does

## Proposed Solution

### 1. Configuration-Driven Approach

Use **CSV files** instead of JSON for configuration (easier to edit, understand, and maintain):

#### `shortcuts-files.csv`

```csv
keyword,name,path,description
scans,Scans,/Volumes/Feral SSD/Dropbox (Personal)/_Personal/_scans,Personal document scans
wtf,WTF,/Volumes/Feral SSD/Dropbox (Personal)/wtf,Folder for Storage of Only the Dankest Maymays
screenshots,Screenshots Folder,/Volumes/Feral SSD/Dropbox (Personal)/Screenshots,Screenshots folder
ndr,Ned Davis Charts,/Volumes/Feral SSD/Dropbox (Personal)/_FERAL/Westwood/assets/charts/ned-davis-charts,Westwood > _assets > charts > ned-davis-charts
www,WWW Directory,~/www,Development projects directory
```

#### `shortcuts-web.csv`

```csv
keyword,name,url,description
cu,Open Clickup Dashboard,https://app.clickup.com/9014243918/dashboards/8cmmwje-13934,ClickUp project management
nas,Feral Creative NAS,https://nas.feralcreative.co,NAS web interface
cloud,Cloudflare Account,https://dash.cloudflare.com/,Cloudflare dashboard
sonarr,Load Sonarr,http://feralcreative.synology.me:8989,Sonarr media management
```

#### `shortcuts-apps.csv`

```csv
keyword,name,path,description
faf,Find any File,/Applications/Find Any File.app,Find Any File application
```

### 2. Workflow Structure

Keep utilities (complex scripts) in the workflow itself, but move simple shortcuts to CSV:

- **Simple shortcuts** (files, web, apps) → CSV-driven
- **Complex utilities** (`gclear`, `>>`) → Keep as workflow objects (they have custom logic)

### 3. Implementation Options

#### Option A: Single Workflow with CSV Backend

- Keep one workflow but read from CSV files
- Python/shell script reads CSV and generates Alfred results
- Easy to add new shortcuts: just edit CSV
- All keywords still work exactly the same

#### Option B: Category-Based Workflows

- Separate workflows: `feral-files`, `feral-web`, `feral-apps`, `feral-utils`
- Each reads from its own CSV (except utils)
- Better organization but more workflows to manage

#### Option C: Hybrid Approach

- One workflow for all shortcuts
- CSV files for data
- Script filter that reads all CSVs and matches keywords
- Utilities remain as separate workflow objects

### 4. Benefits of CSV Approach

✅ **Easy to Edit**: Open in any text editor or spreadsheet app
✅ **Easy to Understand**: Clear column headers, one row per shortcut
✅ **Version Control Friendly**: Git diffs show exactly what changed
✅ **Easy to Add**: Just add a new row
✅ **Easy to Document**: Description column built-in
✅ **No Complex Syntax**: No JSON brackets, quotes, or commas to worry about
✅ **Portable**: Easy to backup, share, or migrate

### 5. Migration Strategy

1. Create CSV files from current plist data
2. Create Python script to read CSVs and handle keywords
3. Test alongside existing workflow
4. Switch over when confident
5. Keep old workflow as backup

## Questions to Resolve

1. **Single workflow vs. multiple?** (Recommendation: Single workflow, easier to manage)
2. **CSV location?** (Recommendation: Inside workflow directory for portability)
3. **How to handle utilities?** (Recommendation: Keep as workflow objects, too complex for CSV)
4. **Discovery feature?** (Could add a `shortcuts` keyword that lists all available shortcuts)

## Implementation Status

✅ **COMPLETE** - Option A implemented successfully!

### What Was Built

1. **CSV Configuration Files**

   - `shortcuts-files.csv` - File/folder shortcuts (5 shortcuts)
   - `shortcuts-web.csv` - Web URL shortcuts (4 shortcuts)
   - `shortcuts-apps.csv` - Application shortcuts (1 shortcut)

2. **Build System**

   - `build-workflow.py` - Generates `info.plist` from CSV files
   - Automatically creates all workflow objects and connections
   - Positions objects on the workflow canvas
   - Includes hardcoded utilities (gclear, >>)

3. **Utilities**

   - `utilities/gclear.sh` - Google Drive cache clearer
   - `utilities/version-snippet.sh` - Version snippet generator

4. **Testing**

   - `test-workflow.py` - Validates all keywords are present
   - All 12 keywords verified working

5. **Documentation**
   - `README.md` - Complete usage guide
   - `REFACTORING_PLAN.md` - This document

### How to Use

**Adding a new shortcut:**

1. Edit the appropriate CSV file
2. Run `python3 build-workflow.py`
3. Review `info.plist.new`
4. Rename to `info.plist`
5. Reload in Alfred

**Example:**

```csv
# Add to shortcuts-web.csv
github,GitHub,https://github.com,GitHub homepage
```

Then:

```bash
python3 build-workflow.py
mv info.plist.new info.plist
```

### Benefits Achieved

✅ All keywords work identically (muscle memory preserved)
✅ CSV files are dead simple to edit
✅ No XML knowledge required
✅ Git-friendly (clear diffs)
✅ Easy to add new shortcuts
✅ Self-documenting (description column)
✅ Scalable to hundreds of shortcuts
✅ Utilities preserved with custom logic

### Files Created

```text
feral-keywords/
├── shortcuts-files.csv          # ← Edit this for file shortcuts
├── shortcuts-web.csv            # ← Edit this for web shortcuts
├── shortcuts-apps.csv           # ← Edit this for app shortcuts
├── utilities/
│   ├── gclear.sh               # Google Drive cache script
│   └── version-snippet.sh      # Version snippet script
├── build-workflow.py            # ← Run this after editing CSVs
├── test-workflow.py             # Validation script
├── info.plist                   # Active workflow (generated)
├── info.plist.backup            # Original workflow backup
├── info.plist.new               # Preview before activating
├── README.md                    # Usage documentation
└── REFACTORING_PLAN.md          # This file
```

### Migration Complete

The old workflow has been backed up to `info.plist.backup` and the new CSV-driven workflow is now active.
