# Feral Folders

A small collection of Finder folder actions for [Alfred](https://www.alfredapp.com/).
It works on macOS only, because Alfred works on macOS only.

Each action is a keyword you trigger against the folder open in the **frontmost
Finder window** — there's no argument to type, just run the keyword.

## Actions

| Keyword  | Action                  | What it does                                                                                             |
| -------- | ----------------------- | -------------------------------------------------------------------------------------------------------- |
| `unfold` | Flatten Folder Hierarchy | Moves every nested file up to the top level, then removes the emptied subfolders. Name collisions get a numeric suffix (`file_1.ext`). Loose files already at the root are left untouched. |
| `defold` | Delete Empty Folders    | Recursively deletes empty folders and subfolders.                                                        |
| `tidy`   | Group Files by Extension | Sorts files into folders named for their (lowercased) extension, so `.JPG` and `.jpg` land together. Extensionless files are left in place. |

## Notes

- All three actions operate on the frontmost Finder window's folder. If no
  Finder window is open, the action reports "No Finder window detected."
- `unfold` and `tidy` move files on disk and `defold` deletes folders, so
  treat them as destructive — there is no undo beyond Finder's own.

## Install

Double-click `Feral Folders.alfredworkflow` to import into Alfred, or from the
repo root run:

```bash
./wf install feral-folders
```

The scripts live inside the workflow's `info.plist`; they're reproduced here
only so they can be reviewed and version-controlled.

<ziad@feralcreative.co>
