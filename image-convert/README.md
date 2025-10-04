# Image Convert - Alfred Workflow

Convert images between PNG and JPEG formats directly from Finder with intelligent format detection.

## Overview

Image Convert is an Alfred workflow that provides seamless image format conversion between PNG and JPEG. It automatically detects the source format and offers the appropriate conversion option, making it easy to quickly convert images without leaving Finder.

## Features

- **Smart Format Detection**: Automatically detects PNG and JPEG files
- **Bidirectional Conversion**: Convert PNG to JPEG and JPEG to PNG
- **High Quality Output**: JPEG conversion uses 90% quality setting
- **Batch Processing**: Convert multiple files at once
- **Preserves Transparency**: PNG conversion maintains alpha channels
- **Same Directory Output**: Converted files are saved alongside originals

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Install Workflow**:
   - Double-click the `feral-image-convert.alfredworkflow` file
   - Alfred will prompt you to install the workflow
   - Click "Import" to add it to your Alfred workflows

## Usage

### File Actions Method

1. In Finder, select one or more image files (PNG or JPEG)
2. Press the Alfred file action shortcut (default: ⌥⌘\)
3. The workflow will automatically detect the file type:
   - **For PNG files**: Select "Convert to JPEG"
   - **For JPEG files**: Select "Convert to PNG"
4. Converted files will be created in the same directory

### Command Line Usage

You can also run the conversion script directly:

```bash
# Convert PNG to JPEG
python3 png_to_jpg.py -j input.png

# Convert JPEG to PNG
python3 png_to_jpg.py -p input.jpg
```

## File Structure

```text
image-convert/
├── png_to_jpg.py                    # Main conversion script
├── info.plist                       # Alfred workflow configuration
├── feral-image-convert.alfredworkflow # Packaged workflow file
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Requirements

- **Alfred 4+** with Powerpack license
- **Python 3.x** with Pillow library
- **macOS**

## Technical Details

- **Quality Settings**: JPEG conversion uses 90% quality for optimal balance
- **Color Mode Handling**: RGBA/LA images are converted to RGB for JPEG compatibility
- **Error Handling**: Comprehensive error reporting for troubleshooting
- **Output Feedback**: Returns converted file paths for Alfred integration

## Troubleshooting

### Installation Issues

- Ensure Python 3 is installed: `python3 --version`
- Install Pillow if missing: `pip3 install Pillow>=10.0.0`
- Check file permissions on the script

### Conversion Issues

- Verify input files are valid PNG or JPEG images
- Ensure write permissions in the target directory
- Check available disk space for output files

## License

MIT License - feel free to modify and distribute.

## Contributing

Issues and pull requests welcome at [https://github.com/feralcreative/alfred](https://github.com/feralcreative/alfred).
