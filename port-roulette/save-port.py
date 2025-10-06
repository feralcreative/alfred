#!/usr/bin/env python3
"""
Port Roulette - Save Port Script
Saves a port assignment when the user actually selects it.
"""

import sys
import os
import json

# Configuration file path - configurable through Alfred's workflow settings
# Read config directory from Alfred's user configuration
HOME_DIR = os.environ.get('HOME') or os.path.expanduser('~')
USER_CONFIG_DIR = os.environ.get('config_dir', '').strip()

if USER_CONFIG_DIR:
    # User has configured a custom directory
    CONFIG_DIR = os.path.expanduser(USER_CONFIG_DIR)
    CONFIG_FILE = os.path.join(CONFIG_DIR, "port-roulette-config.json")
else:
    # Use fallback location in home directory
    CONFIG_FILE = os.path.join(HOME_DIR, '.port-roulette-config.json')

# Always have a fallback
FALLBACK_CONFIG_FILE = os.path.join(HOME_DIR, '.port-roulette-config.json')

def get_config_file():
    """Get the config file path, preferring user configuration but falling back if needed"""
    if USER_CONFIG_DIR:
        try:
            # User has configured a custom directory - try to use it
            config_dir = os.path.dirname(CONFIG_FILE)
            os.makedirs(config_dir, exist_ok=True)
            # Test if we can write to it
            test_file = os.path.join(config_dir, '.test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return CONFIG_FILE
        except (OSError, IOError):
            # Custom directory failed, fall back
            pass
    
    # Use fallback location
    return FALLBACK_CONFIG_FILE

def load_config():
    """Load configuration from file"""
    config_file = get_config_file()
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return {"projects": {}, "used_ports": []}

def save_config(config):
    """Save configuration to file"""
    config_file = get_config_file()
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError:
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: save-port.py save:project_name:port")
        return

    arg = sys.argv[1]
    
    # Parse the argument: save:project_name:port
    if not arg.startswith("save:"):
        # If it's just a port number, copy it to clipboard and exit
        print(arg)
        return
    
    try:
        _, project_name, port_str = arg.split(":", 2)
        port = int(port_str)
    except (ValueError, IndexError):
        print("Invalid argument format")
        return
    
    # Load config and save the port assignment
    config = load_config()
    config.setdefault("projects", {})[project_name] = port
    if port not in config.setdefault("used_ports", []):
        config["used_ports"].append(port)
    
    save_config(config)
    
    # Output the port number for clipboard
    print(port)

if __name__ == "__main__":
    main()
