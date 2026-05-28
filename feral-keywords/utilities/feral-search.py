#!/usr/bin/env python3
"""
Search files in _FERAL directory using Spotlight (mdfind)
Returns Alfred Script Filter JSON results
"""

import os
import sys
import json
import subprocess

CANDIDATE_DIRS = [
    "/Volumes/Feral SSD/Dropbox (Personal)/_FERAL",
    os.path.expanduser("~/Library/CloudStorage/Dropbox-Personal/_FERAL"),
    os.path.expanduser("~/Library/CloudStorage/Dropbox-Personal1/_FERAL"),
]
SEARCH_DIRS = [p for p in CANDIDATE_DIRS if os.path.isdir(p)]

def get_file_icon(file_path):
    """Get appropriate icon for file type"""
    if os.path.isdir(file_path):
        return {"type": "fileicon", "path": file_path}
    else:
        return {"type": "fileicon", "path": file_path}

def search_files(query, max_results=200):
    """Search files across all existing _FERAL directories using Spotlight.

    Iterates every candidate dir that exists on this machine; missing ones
    are skipped silently. Per-directory errors are also swallowed so a
    flaky volume doesn't break the whole search.
    """
    if not SEARCH_DIRS:
        return [{
            "title": "No _FERAL directories found",
            "subtitle": "Checked: " + ", ".join(CANDIDATE_DIRS),
            "valid": False
        }]

    scored_results = []
    seen_paths = set()

    for search_dir in SEARCH_DIRS:
        try:
            if not query or len(query) < 1:
                for item in sorted(os.listdir(search_dir)):
                    if item.startswith('.'):
                        continue
                    item_path = os.path.join(search_dir, item)
                    if item_path in seen_paths:
                        continue
                    seen_paths.add(item_path)
                    scored_results.append({
                        "score": 0,
                        "title": item,
                        "subtitle": item,
                        "arg": item_path,
                        "type": "file",
                        "icon": get_file_icon(item_path)
                    })
                continue

            cmd = [
                'mdfind',
                '-onlyin', search_dir,
                f'kMDItemFSName == "*{query}*"c'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                continue

            for file_path in result.stdout.strip().split('\n'):
                if not file_path or file_path in seen_paths:
                    continue
                if not os.path.exists(file_path):
                    continue
                filename = os.path.basename(file_path)
                if filename.startswith('.'):
                    continue
                seen_paths.add(file_path)
                depth = file_path.count('/') - search_dir.count('/')
                rel_path = os.path.relpath(file_path, search_dir)
                scored_results.append({
                    "score": depth,
                    "title": filename,
                    "subtitle": rel_path,
                    "arg": file_path,
                    "type": "file",
                    "icon": get_file_icon(file_path)
                })
        except (subprocess.TimeoutExpired, OSError):
            continue

    scored_results.sort(key=lambda x: (x['score'], x['title'].lower()))

    results = []
    for item in scored_results[:max_results]:
        del item['score']
        results.append(item)

    if not results:
        return [{
            "title": "No results found",
            "subtitle": "No files found in _FERAL",
            "valid": False
        }]

    return results

def main():
    """Main function

    When alfredfiltersresults is enabled in the workflow, Alfred handles
    the filtering. The script should return all results regardless of query.
    """
    # Ignore the query parameter - Alfred will filter the results
    # We pass empty string to get all top-level items
    results = search_files("")

    output = {"items": results}
    print(json.dumps(output))

if __name__ == "__main__":
    main()
