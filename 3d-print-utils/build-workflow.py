#!/usr/bin/env python3
"""Build 3D Print Utils workflow - opens model search across multiple sites"""

import uuid
import plistlib

KEYWORD = '3d'
KEYWORD_TITLE = 'Search 3D Models'
KEYWORD_SUBTEXT = 'Search Printables, Thingiverse, Thangs, MakerWorld'

URLS = [
    'https://www.printables.com/search/models?q={query}',
    'https://www.thingiverse.com/search?q={query}&page=1',
    'https://thangs.com/search/{query}?searchScope=thangs',
    'https://makerworld.com/en/search/models?keyword={query}',
]

def uid():
    return str(uuid.uuid4()).upper()

keyword_uid = uid()

url_objects = []
for url in URLS:
    url_objects.append({
        'config': {
            'browser': 'at.obdev.Choosy',
            'skipqueryencode': False,
            'skipvarencode': False,
            'spaces': '',
            'url': url,
        },
        'type': 'alfred.workflow.action.openurl',
        'uid': uid(),
        'version': 1,
    })

keyword_obj = {
    'config': {
        'argumenttype': 0,  # required argument
        'keyword': KEYWORD,
        'subtext': KEYWORD_SUBTEXT,
        'text': KEYWORD_TITLE,
        'withspace': True,
    },
    'type': 'alfred.workflow.input.keyword',
    'uid': keyword_uid,
    'version': 1,
}

objects = [keyword_obj] + url_objects

connections = {
    keyword_uid: [
        {
            'destinationuid': obj['uid'],
            'modifiers': 0,
            'modifiersubtext': '',
            'vitoclose': False,
        }
        for obj in url_objects
    ]
}

uidata = {keyword_uid: {'xpos': 90.0, 'ypos': 100.0}}
for i, obj in enumerate(url_objects):
    uidata[obj['uid']] = {'xpos': 340.0, 'ypos': float(100 + i * 90)}

plist = {
    'bundleid': 'co.feralcreative.3dprintutils',
    'category': 'Tools',
    'connections': connections,
    'createdby': 'Ziad Ezzat',
    'description': 'Search 3D model sites simultaneously',
    'disabled': False,
    'name': '3D Print Utils',
    'objects': objects,
    'uidata': uidata,
    'version': '1.0',
    'webaddress': 'https://github.com/feralcreative/alfred',
}

with open('info.plist', 'wb') as f:
    plistlib.dump(plist, f)

import subprocess
subprocess.run(['zip', '-j', '3D Print Utils.alfredworkflow', 'info.plist', 'icon.png'], check=True)

print(f"Generated '3D Print Utils.alfredworkflow' with keyword '{KEYWORD}' -> {len(url_objects)} URL actions")
