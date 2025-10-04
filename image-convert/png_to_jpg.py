#!/usr/bin/env python3
import sys
import os
from PIL import Image

def convert_image(input_path, to_png=False):
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB mode if needed
            if img.mode in ('RGBA', 'LA') and not to_png:
                img = img.convert('RGB')
            
            # Determine the output extension and format
            base_path = input_path.rsplit('.', 1)[0]
            if to_png:
                output_path = base_path + '.png'
                save_format = 'PNG'
            else:
                output_path = base_path + '.jpg'
                save_format = 'JPEG'
            
            # Save with appropriate format and settings
            if save_format == 'JPEG':
                img.save(output_path, save_format, quality=90)
            else:
                img.save(output_path, save_format)
            
            print(output_path)  # Output the new file path for Alfred
            return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Error: Please provide direction flag (-p for to PNG, -j for to JPG) and file path", file=sys.stderr)
        sys.exit(1)
    
    flag, file_path = sys.argv[1:3]
    if flag not in ['-p', '-j']:
        print("Error: Invalid flag. Use -p for PNG output or -j for JPG output", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(convert_image(file_path, to_png=(flag == '-p')))
