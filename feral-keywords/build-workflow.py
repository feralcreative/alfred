#!/usr/bin/env python3
"""
Build Feral Keywords workflow from CSV files
Generates info.plist with all shortcuts as individual keyword triggers
"""

import csv
import os
import uuid
import plistlib
from datetime import datetime

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
    # Check for PNG, JPG, or SVG
    for ext in ['png', 'jpg', 'jpeg', 'svg']:
        icon_path = f'icons/{keyword}.{ext}'
        if os.path.exists(icon_path):
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

def build_workflow():
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
Utils: gclear, >>

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
        'version': '2.0',
        'webaddress': 'http://feralcreative.co'
    }

    return plist

def main():
    """Main build function"""
    print("Building Feral Keywords workflow from CSV files...")

    # Build the workflow
    plist = build_workflow()

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
