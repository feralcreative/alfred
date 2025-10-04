# Image Format Converter for Alfred

This Alfred workflow converts images between PNG and JPEG formats.

## Setup

1. Install the required Python package:
   ```
   pip3 install -r requirements.txt
   ```

2. Import the workflow into Alfred by double-clicking the workflow directory.

## Usage

1. In Finder, select one or more image files (PNG or JPEG)
2. Press the Alfred file action shortcut (default is ⌥⌘\)
3. The workflow will automatically detect the file type:
   - For PNG files: Select "Convert to JPEG"
   - For JPEG files: Select "Convert to PNG"
4. The script will create converted versions of your files in the same directory

The converted files will be created alongside the original files with the appropriate extension (.jpg or .png).

## Manual Usage
You can also run the script directly from the command line:

```bash
# Convert PNG to JPEG
python3 png_to_jpg.py -j input.png

# Convert JPEG to PNG
python3 png_to_jpg.py -p input.jpg
