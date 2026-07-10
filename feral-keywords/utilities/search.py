#!/usr/bin/env python3
"""
Recursively search a folder and return Alfred Script Filter JSON.

Usage:
    search.py [--engine walk|spotlight] [--types files|dirs|all] "<scope>" "<query>"

Two engines:
  walk       - os.walk the tree in-process. Exhaustive (no Spotlight gaps) but
               O(tree size); good for modest folders.
  spotlight  - mdfind (Spotlight index). Effectively instant regardless of tree
               size; the only sane choice for very large trees, at the cost of
               whatever Spotlight hasn't indexed.

The query is split on whitespace into terms; every term must match (AND). Each
result's arg is the full path so a downstream Reveal-in-Finder action opens the
match's enclosing folder with it selected.
"""

import argparse
import json
import os
import subprocess
import sys

MAX_RESULTS = 100
# Path segments we never want in results.
SKIP_SEGMENTS = {'node_modules', '.git', '.svn'}


def emit(items):
    print(json.dumps({"items": items}))


def is_skipped(rel_parts):
    """True if any path segment is junk or a dotdir/dotfile."""
    return any(p in SKIP_SEGMENTS or p.startswith('.') for p in rel_parts)


def make_item(full, scope, is_dir):
    rel = os.path.relpath(full, scope)
    name = os.path.basename(full.rstrip('/'))
    return {
        "title": name + ('/' if is_dir else ''),
        "subtitle": rel,
        "arg": full,
        "type": "file",
        "icon": {"type": "fileicon", "path": full},
    }


def rank_key(full, terms):
    name = os.path.basename(full.rstrip('/')).lower()
    in_name = all(t in name for t in terms)
    depth = full.rstrip('/').count(os.sep)
    return (0 if in_name else 1, depth, len(name), name)


def search_walk(scope, terms, want_files, want_dirs):
    out = []
    for root, dirs, files in os.walk(scope):
        dirs[:] = [d for d in dirs if d not in SKIP_SEGMENTS and not d.startswith('.')]
        candidates = []
        if want_dirs:
            candidates += [(os.path.join(root, d), True) for d in dirs]
        if want_files:
            candidates += [(os.path.join(root, f), False) for f in files if not f.startswith('.')]
        for full, is_dir in candidates:
            hay = os.path.relpath(full, scope).lower()
            if all(t in hay for t in terms):
                out.append((full, is_dir))
    return out


def mdfind_stream(scope, expr, read_cap):
    """Yield raw paths from a streaming mdfind, bounded to read_cap lines.

    Streaming + a read cap keeps latency bounded even when a term matches
    hundreds of thousands of files (mdfind can't exclude node_modules itself).
    """
    try:
        proc = subprocess.Popen(
            ['mdfind', '-onlyin', scope, expr],
            stdout=subprocess.PIPE, text=True
        )
    except OSError:
        return
    try:
        for read, line in enumerate(proc.stdout, start=1):
            full = line.rstrip('\n')
            if full:
                yield full
            if read >= read_cap:
                break
    finally:
        proc.kill()
        try:
            proc.stdout.close()
        except OSError:
            pass


def search_spotlight(scope, terms, want_files, want_dirs):
    # Query mdfind on just the most-selective (longest) term, then post-filter
    # so ALL terms appear in the relative path — same semantics as the walk
    # engine, so folder+file queries like "feral header" work. Querying one
    # narrow term (rather than ANDing them all in the filename) also keeps the
    # stream small. Junk is dropped inline; caps bound how much we read/keep.
    READ_CAP = 20000
    KEEP_CAP = 500
    selective = max(terms, key=len)
    clauses = ['kMDItemFSName == "*%s*"c' % selective.replace('"', '')]
    if want_dirs and not want_files:
        clauses.append('kMDItemContentType == "public.folder"')
    elif want_files and not want_dirs:
        clauses.append('kMDItemContentType != "public.folder"')
    expr = ' && '.join(clauses)

    out = []
    for full in mdfind_stream(scope, expr, READ_CAP):
        rel = os.path.relpath(full, scope)
        parts = rel.split(os.sep)
        if is_skipped(parts):
            continue
        if not all(t in rel.lower() for t in terms):
            continue
        if not os.path.exists(full):
            continue
        out.append((full, os.path.isdir(full)))
        if len(out) >= KEEP_CAP:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', choices=['walk', 'spotlight'], default='walk')
    ap.add_argument('--types', choices=['files', 'dirs', 'all'], default='files')
    ap.add_argument('scope')
    ap.add_argument('query', nargs='?', default='')
    args = ap.parse_args()

    scope = os.path.expanduser(args.scope)
    query = args.query.strip()

    if not scope or not os.path.isdir(scope):
        emit([{"title": "Search folder not found", "subtitle": scope or "(no path given)", "valid": False}])
        return

    if not query:
        emit([{"title": "Type to search…", "subtitle": f"Searches {scope}", "valid": False}])
        return

    terms = [t.lower() for t in query.split() if t]
    want_files = args.types in ('files', 'all')
    want_dirs = args.types in ('dirs', 'all')

    if args.engine == 'spotlight':
        matches = search_spotlight(scope, terms, want_files, want_dirs)
    else:
        matches = search_walk(scope, terms, want_files, want_dirs)

    # Dedupe, then rank.
    seen = set()
    unique = []
    for full, is_dir in matches:
        if full in seen:
            continue
        seen.add(full)
        unique.append((full, is_dir))

    unique.sort(key=lambda pair: rank_key(pair[0], terms))
    items = [make_item(full, scope, is_dir) for full, is_dir in unique[:MAX_RESULTS]]

    if not items:
        emit([{"title": "No matches", "subtitle": f"Nothing matching “{query}” in {os.path.basename(scope)}", "valid": False}])
        return

    emit(items)


if __name__ == "__main__":
    main()
