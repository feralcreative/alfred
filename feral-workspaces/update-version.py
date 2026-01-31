#!/usr/bin/env python3
"""
Update version in feral-workspaces info.plist
"""

import re
import sys
import os

def get_current_version():
    """Read current version from existing info.plist, or return default"""
    if os.path.exists('info.plist'):
        try:
            with open('info.plist', 'r', encoding='utf-8') as f:
                content = f.read()
                # Find the main workflow version (after variablesdontexport)
                match = re.search(r'<key>variablesdontexport</key>.*?<key>version</key>\s*<string>([^<]+)</string>', content, re.DOTALL)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"Warning: Could not read current version: {e}")
    return '1.0'  # Default version

def increment_version(current_version, major_update=False):
    """Increment version number"""
    try:
        version_float = float(current_version)
        if major_update:
            # Round up to next tenth
            major_part = int(version_float)
            minor_part = int((version_float - major_part) * 100)
            if minor_part == 0:
                new_version = f"{major_part}.1"
            else:
                new_minor = ((minor_part // 10) + 1) * 10
                if new_minor >= 100:
                    new_version = f"{major_part + 1}.0"
                else:
                    new_version = f"{major_part}.{new_minor}"
        else:
            # Increment by 0.01
            new_version = f"{version_float + 0.01:.2f}"
        return new_version
    except ValueError:
        print(f"Warning: Invalid version format '{current_version}', using default increment")
        return "1.01"

def update_version_in_plist(new_version):
    """Update version in info.plist file"""
    if not os.path.exists('info.plist'):
        print("Error: info.plist not found")
        return False
    
    try:
        with open('info.plist', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the version after variablesdontexport
        pattern = r'(<key>variablesdontexport</key>.*?<key>version</key>\s*<string>)[^<]+(<\/string>)'
        replacement = f'\\g<1>{new_version}\\g<2>'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open('info.plist', 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            print("Warning: No version found to update")
            return False
    except Exception as e:
        print(f"Error updating version: {e}")
        return False

def main():
    """Main function"""
    major_update = '--major' in sys.argv
    
    current_version = get_current_version()
    new_version = increment_version(current_version, major_update)
    
    print(f"Version: {current_version} → {new_version}" + (" (major)" if major_update else " (minor)"))
    
    if update_version_in_plist(new_version):
        print("✅ Version updated successfully")
        return True
    else:
        print("❌ Version update failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
