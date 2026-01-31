#!/usr/bin/env python3
"""
Build Feral Keywords workflow from CSV files
Generates info.plist with all shortcuts as individual keyword triggers
"""

import csv
import os
import uuid
import plistlib
import re
from datetime import datetime

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
    return '2.0'  # Default version

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
        return "2.01"

def read_csv_shortcuts(csv_file):
    """Read shortcuts from a CSV file"""
    shortcuts = []
    if not os.path.exists(csv_file):
        return shortcuts

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shortcuts.append(row)

    return shortcuts

def get_icon_path(keyword):
    """Get custom icon path if it exists, otherwise return None"""
    # Check for PNG only
    icon_path = f'icons/{keyword}.png'
    if os.path.exists(icon_path):
        # Return relative path for Alfred (relative to workflow directory)
        return {'path': icon_path}
    return None

def create_keyword_object(keyword, name, subtext="", icon_path=None):
    """Create a keyword input object"""
    config = {
        'argumenttype': 2,  # No argument
        'keyword': keyword or '',
        'subtext': subtext or '',
        'text': name or '',
        'withspace': False
    }

    obj = {
        'config': config,
        'type': 'alfred.workflow.input.keyword',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1
    }

    # Add custom icon if provided
    if icon_path:
        obj['config']['icon'] = icon_path

    return obj

def create_open_url_object(url):
    """Create an open URL action object"""
    return {
        'config': {
            'browser': '',
            'skipqueryencode': False,
            'skipvarencode': False,
            'spaces': '',
            'url': url or ''
        },
        'type': 'alfred.workflow.action.openurl',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1
    }

def create_launch_file_object(path):
    """Create a launch file/folder action object"""
    return {
        'config': {
            'paths': [path or ''],
            'toggle': False
        },
        'type': 'alfred.workflow.action.launchfiles',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1
    }

def create_connection(source_uid, dest_uid):
    """Create a connection between two objects"""
    return {
        'destinationuid': dest_uid,
        'modifiers': 0,
        'modifiersubtext': '',
        'vitoclose': False
    }

def create_script_object(script_content, script_type=5):
    """Create a shell script action object"""
    return {
        'config': {
            'concurrently': False,
            'escaping': 102,
            'script': script_content,
            'scriptargtype': 1,
            'scriptfile': '',
            'type': script_type
        },
        'type': 'alfred.workflow.action.script',
        'uid': str(uuid.uuid4()).upper(),
        'version': 2
    }

def create_paste_action():
    """Create a Cmd+V paste action"""
    return {
        'config': {
            'count': 1,
            'keychar': 'v',
            'keycode': -1,
            'keymod': 1048576,
            'overridewithargument': False
        },
        'type': 'alfred.workflow.output.dispatchkeycombo',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1
    }

def create_script_filter_object(keyword, name, subtext, script_content, icon_path=None):
    """Create a script filter object"""
    config = {
        'alfredfiltersresults': False,
        'alfredfiltersresultsmatchmode': 0,
        'argumenttreatemptyqueryasnil': True,
        'argumenttrimmode': 0,
        'argumenttype': 1,  # Optional argument
        'escaping': 102,
        'keyword': keyword or '',
        'queuedelaycustom': 3,
        'queuedelayimmediatelyinitially': True,
        'queuedelaymode': 0,
        'queuemode': 1,
        'runningsubtext': 'Searching...',
        'script': script_content,
        'scriptargtype': 1,
        'scriptfile': '',
        'subtext': subtext or '',
        'title': name or '',
        'type': 0,  # Bash script
        'withspace': True
    }

    obj = {
        'config': config,
        'type': 'alfred.workflow.input.scriptfilter',
        'uid': str(uuid.uuid4()).upper(),
        'version': 3
    }

    # Add custom icon if provided
    if icon_path:
        obj['config']['icon'] = icon_path

    return obj

def create_open_file_action():
    """Create an action to open a file"""
    return {
        'config': {
            'acceptsmulti': False,
            'filetypes': [],
            'name': 'Open'
        },
        'type': 'alfred.workflow.action.openfile',
        'uid': str(uuid.uuid4()).upper(),
        'version': 3
    }

def build_workflow(new_version='2.0'):
    """Build the complete workflow plist"""
    
    # Read all shortcuts
    file_shortcuts = read_csv_shortcuts('shortcuts-files.csv')
    web_shortcuts = read_csv_shortcuts('shortcuts-web.csv')
    app_shortcuts = read_csv_shortcuts('shortcuts-apps.csv')
    
    objects = []
    connections = {}
    uidata = {}
    
    y_position = 100
    x_input = 90
    x_action = 270
    y_spacing = 110
    
    # Process file shortcuts
    for shortcut in file_shortcuts:
        icon = get_icon_path(shortcut['keyword'])
        keyword_obj = create_keyword_object(
            shortcut['keyword'],
            shortcut['name'],
            shortcut.get('description', ''),
            icon
        )
        action_obj = create_launch_file_object(shortcut['path'])
        
        objects.append(keyword_obj)
        objects.append(action_obj)
        
        # Create connection
        connections[keyword_obj['uid']] = [
            create_connection(keyword_obj['uid'], action_obj['uid'])
        ]
        
        # Set positions
        uidata[keyword_obj['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
        uidata[action_obj['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}
        
        y_position += y_spacing
    
    # Process web shortcuts
    for shortcut in web_shortcuts:
        icon = get_icon_path(shortcut['keyword'])
        keyword_obj = create_keyword_object(
            shortcut['keyword'],
            shortcut['name'],
            shortcut.get('description', ''),
            icon
        )
        action_obj = create_open_url_object(shortcut['url'])
        
        objects.append(keyword_obj)
        objects.append(action_obj)
        
        connections[keyword_obj['uid']] = [
            create_connection(keyword_obj['uid'], action_obj['uid'])
        ]
        
        uidata[keyword_obj['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
        uidata[action_obj['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}

        y_position += y_spacing

    # Process app shortcuts
    for shortcut in app_shortcuts:
        icon = get_icon_path(shortcut['keyword'])
        keyword_obj = create_keyword_object(
            shortcut['keyword'],
            shortcut['name'],
            shortcut.get('description', ''),
            icon
        )
        action_obj = create_launch_file_object(shortcut['path'])

        objects.append(keyword_obj)
        objects.append(action_obj)

        connections[keyword_obj['uid']] = [
            create_connection(keyword_obj['uid'], action_obj['uid'])
        ]

        uidata[keyword_obj['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
        uidata[action_obj['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}

        y_position += y_spacing

    # Add utility: gclear (Google Drive cache clear)
    gclear_icon = get_icon_path('gclear')
    gclear_keyword = create_keyword_object(
        'gclear',
        'Clear Drive Cache',
        'Clear Google File Stream Cache',
        gclear_icon
    )
    gclear_script_content = open('utilities/gclear.sh', 'r').read()
    gclear_action = create_script_object(gclear_script_content)

    objects.append(gclear_keyword)
    objects.append(gclear_action)
    connections[gclear_keyword['uid']] = [
        create_connection(gclear_keyword['uid'], gclear_action['uid'])
    ]
    uidata[gclear_keyword['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
    uidata[gclear_action['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}
    y_position += y_spacing

    # Add utility: >> (version snippet generator)
    version_keyword = {
        'config': {
            'argumenttype': 0,  # Required argument
            'keyword': '>>',
            'subtext': '// v00.00 - 0000.00.00.0000',
            'text': 'Version Snippet',
            'withspace': True
        },
        'type': 'alfred.workflow.input.keyword',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1
    }
    version_script_content = open('utilities/version-snippet.sh', 'r').read()
    version_script = create_script_object(version_script_content)
    version_paste = create_paste_action()

    objects.append(version_keyword)
    objects.append(version_script)
    objects.append(version_paste)

    connections[version_keyword['uid']] = [
        create_connection(version_keyword['uid'], version_script['uid'])
    ]
    connections[version_script['uid']] = [
        create_connection(version_script['uid'], version_paste['uid'])
    ]

    uidata[version_keyword['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
    uidata[version_script['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}
    uidata[version_paste['uid']] = {'xpos': float(x_action + 180), 'ypos': float(y_position)}
    y_position += y_spacing

    # Add utility: fe (file search in _FERAL directory)
    fe_icon = get_icon_path('fe')
    # Use bash wrapper to call Python script
    fe_script_content = '/usr/bin/python3 ./utilities/feral-search.py "$1"'
    feral_filter = create_script_filter_object(
        'fe',
        'Search _FERAL',
        'Search files in _FERAL directory',
        fe_script_content,
        fe_icon
    )
    feral_open = create_open_file_action()

    objects.append(feral_filter)
    objects.append(feral_open)
    connections[feral_filter['uid']] = [
        create_connection(feral_filter['uid'], feral_open['uid'])
    ]
    uidata[feral_filter['uid']] = {'xpos': float(x_input), 'ypos': float(y_position)}
    uidata[feral_open['uid']] = {'xpos': float(x_action), 'ypos': float(y_position)}
    y_position += y_spacing

    # Build the complete plist structure
    readme_text = """# Feral Keywords - CSV-Driven Workflow

This workflow is now CSV-driven for easy maintenance.

## Quick Start

1. Edit CSV files to add/modify shortcuts:
   - shortcuts-files.csv (file/folder shortcuts)
   - shortcuts-web.csv (web shortcuts)
   - shortcuts-apps.csv (app shortcuts)

2. Rebuild the workflow:
   ./rebuild.sh

3. Reload in Alfred

## Current Shortcuts

Files: scans, wtf, screenshots, ndr, www
Web: cu, nas, cloud, sonarr
Apps: faf
Utils: gclear, >>, fe

See README.md for full documentation.
"""

    plist = {
        'bundleid': 'co.feralcreative.keywords',
        'category': 'Tools',
        'connections': connections,
        'createdby': 'Ziad Ezzat',
        'description': 'CSV-driven shortcuts for files, web, and apps',
        'disabled': False,
        'name': 'Feral Keywords',
        'objects': objects,
        'readme': readme_text,
        'uidata': uidata,
        'userconfigurationconfig': [],
        'variablesdontexport': [],
        'version': new_version,
        'webaddress': 'http://feralcreative.co'
    }

    return plist

def main():
    """Main build function"""
    import sys

    # Check for major update flag
    major_update = '--major' in sys.argv

    print("Building Feral Keywords workflow from CSV files...")

    # Get current version and increment it
    current_version = get_current_version()
    new_version = increment_version(current_version, major_update)

    print(f"Version: {current_version} → {new_version}" + (" (major)" if major_update else " (minor)"))

    # Build the workflow with new version
    plist = build_workflow(new_version)

    # Write to info.plist
    with open('info.plist.new', 'wb') as f:
        plistlib.dump(plist, f)

    print(f"✓ Generated info.plist.new with {len(plist['objects'])} objects")
    print(f"  - {len([o for o in plist['objects'] if o['type'] == 'alfred.workflow.input.keyword'])} keywords")
    print(f"  - {len([o for o in plist['objects'] if o['type'] == 'alfred.workflow.action.openurl'])} web shortcuts")
    print(f"  - {len([o for o in plist['objects'] if o['type'] == 'alfred.workflow.action.launchfiles'])} file/app shortcuts")
    print("\nReview info.plist.new, then rename to info.plist to activate")

if __name__ == "__main__":
    main()
