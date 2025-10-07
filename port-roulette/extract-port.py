#!/usr/bin/env python3
"""
Extract Port - Alfred Workflow Helper
Extracts just the port number from the save:project:port format for clipboard
"""

import sys

def main():
    if len(sys.argv) < 2:
        print("Error: No argument provided")
        return

    arg = sys.argv[1].strip()
    
    # Parse the save:project:port format and extract just the port
    if arg.startswith("save:"):
        try:
            _, project_name, port_str = arg.split(":", 2)
            print(port_str)
        except (ValueError, IndexError):
            print("Error: Invalid argument format")
    else:
        # If it's not in save format, just pass it through
        print(arg)

if __name__ == "__main__":
    main()
