#!/usr/bin/env python3
"""
Test script to verify the generated workflow has all expected keywords
"""

import plistlib
import sys

def test_workflow():
    """Test the generated workflow"""
    
    # Expected keywords from CSV files
    expected_keywords = {
        # File shortcuts
        'scans', 'wtf', 'screenshots', 'ndr', 'www',
        # Web shortcuts
        'cu', 'nas', 'cloud', 'sonarr',
        # App shortcuts
        'faf',
        # Utilities
        'gclear', '>>'
    }
    
    # Read the plist
    with open('info.plist', 'rb') as f:
        plist = plistlib.load(f)
    
    # Extract all keywords
    found_keywords = set()
    for obj in plist.get('objects', []):
        if obj.get('type') == 'alfred.workflow.input.keyword':
            keyword = obj.get('config', {}).get('keyword', '')
            if keyword:
                found_keywords.add(keyword)
    
    # Check for missing keywords
    missing = expected_keywords - found_keywords
    extra = found_keywords - expected_keywords
    
    print("Workflow Test Results")
    print("=" * 50)
    print(f"Expected keywords: {len(expected_keywords)}")
    print(f"Found keywords: {len(found_keywords)}")
    print()
    
    if missing:
        print("❌ MISSING KEYWORDS:")
        for kw in sorted(missing):
            print(f"  - {kw}")
        print()
    
    if extra:
        print("⚠️  EXTRA KEYWORDS:")
        for kw in sorted(extra):
            print(f"  - {kw}")
        print()
    
    if not missing and not extra:
        print("✅ All keywords present and accounted for!")
        print()
        print("Found keywords:")
        for kw in sorted(found_keywords):
            print(f"  - {kw}")
        return True
    
    return False

if __name__ == "__main__":
    success = test_workflow()
    sys.exit(0 if success else 1)

