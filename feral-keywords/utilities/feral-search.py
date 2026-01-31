#!/usr/bin/env python3
"""
Search files in _FERAL directory using Spotlight (mdfind)
Returns Alfred Script Filter JSON results
"""

import os
import sys
import json
import subprocess

SEARCH_DIR = "/Volumes/Feral SSD/Dropbox (Personal)/_FERAL"

def get_file_icon(file_path):
    """Get appropriate icon for file type"""
    if os.path.isdir(file_path):
        return {"type": "fileicon", "path": file_path}
    else:
        return {"type": "fileicon", "path": file_path}

def search_files(query, max_results=50):
    """Search for files matching query in _FERAL directory using Spotlight"""
    results = []

    # Check if directory exists
    if not os.path.exists(SEARCH_DIR):
        return [{
            "title": "Directory not found",
            "subtitle": SEARCH_DIR,
            "valid": False
        }]

    # If no query, show top-level items
    if not query:
        try:
            for item in sorted(os.listdir(SEARCH_DIR)):
                if item.startswith('.'):
                    continue
                item_path = os.path.join(SEARCH_DIR, item)
                results.append({
                    "title": item,
                    "subtitle": item_path,
                    "arg": item_path,
                    "type": "file",
                    "icon": get_file_icon(item_path)
                })
                if len(results) >= max_results:
                    break
        except Exception as e:
            return [{
                "title": "Error reading directory",
                "subtitle": str(e),
                "valid": False
            }]
    else:
        # Use mdfind (Spotlight) for fast searching
        try:
            # Search for files with name containing query in SEARCH_DIR
            cmd = [
                'mdfind',
                '-onlyin', SEARCH_DIR,
                f'kMDItemFSName == "*{query}*"c'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                paths = result.stdout.strip().split('\n')
                paths = [p for p in paths if p]  # Remove empty strings

                # Build results with relevance scoring
                scored_results = []
                query_lower = query.lower()

                for file_path in paths:
                    if not os.path.exists(file_path):
                        continue

                    filename = os.path.basename(file_path)
                    filename_lower = filename.lower()

                    # Calculate relevance score (lower is better)
                    # 1. Exact match = 0
                    # 2. Starts with query = 1
                    # 3. Contains query = position where it appears
                    # 4. Add depth penalty
                    if filename_lower == query_lower:
                        score = 0
                    elif filename_lower.startswith(query_lower):
                        score = 1
                    else:
                        score = filename_lower.find(query_lower) + 2

                    # Add depth penalty (prefer shallower files)
                    depth = file_path.count('/') - SEARCH_DIR.count('/')
                    score += depth * 100

                    rel_path = os.path.relpath(file_path, SEARCH_DIR)

                    scored_results.append({
                        "score": score,
                        "title": filename,
                        "subtitle": rel_path,
                        "arg": file_path,
                        "type": "file",
                        "icon": get_file_icon(file_path)
                    })

                # Sort by score, then alphabetically
                scored_results.sort(key=lambda x: (x['score'], x['title'].lower()))

                # Remove score from results and limit to max_results
                for item in scored_results[:max_results]:
                    del item['score']
                    results.append(item)
            else:
                return [{
                    "title": "Search error",
                    "subtitle": result.stderr or "mdfind failed",
                    "valid": False
                }]

        except subprocess.TimeoutExpired:
            return [{
                "title": "Search timeout",
                "subtitle": "Search took too long",
                "valid": False
            }]
        except Exception as e:
            return [{
                "title": "Error searching",
                "subtitle": str(e),
                "valid": False
            }]

    if not results:
        return [{
            "title": "No results found",
            "subtitle": f"No files matching '{query}' in _FERAL",
            "valid": False
        }]

    return results

def main():
    """Main function"""
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    results = search_files(query)
    
    output = {"items": results}
    print(json.dumps(output))

if __name__ == "__main__":
    main()
