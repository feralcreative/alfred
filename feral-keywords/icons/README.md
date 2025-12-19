# Custom Icons

Place custom icons in this folder to override the default icons for keywords.

## Naming Convention

Icons should be named after the keyword:

```text
{keyword}.png
{keyword}.jpg
{keyword}.svg
```

## Supported Formats

- PNG (recommended)
- JPG/JPEG
- SVG

## Examples

```text
icons/
├── cu.png          # ClickUp icon
├── nas.png         # NAS icon
├── sonarr.png      # Sonarr icon
├── radarr.png      # Radarr icon
└── gclear.svg      # Google Drive clear icon
```

## Icon Size

Recommended size: 256x256 pixels (PNG) or vector (SVG)

## Default Behavior

If no custom icon is found, Alfred uses:
- **File shortcuts**: The actual folder/file icon from macOS
- **Web shortcuts**: System bookmark icon
- **App shortcuts**: The application's icon

## Adding Icons

1. Save your icon as `{keyword}.png` (or .jpg/.svg)
2. Place it in this `icons/` folder
3. Run `./rebuild.sh`
4. Reload workflow in Alfred

The build script automatically detects and uses custom icons.

