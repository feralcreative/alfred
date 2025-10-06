#!/usr/bin/env python3
"""
Port Roulette - Alfred Workflow
Generates unique port numbers for development projects
"""

import sys
import json
import os
import re
from pathlib import Path

# Configuration file path - can be customized by changing this line
# Default: ~/www/_vscode/port-roulette-config.json
# Alternative: ~/.port-roulette-config.json (original location)
CONFIG_DIR = os.path.expanduser("~/www/_vscode")
CONFIG_FILE = os.path.join(CONFIG_DIR, "port-roulette-config.json")

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# Well-known ports to avoid (System Ports 0-1023 and common application ports)
WELL_KNOWN_PORTS = {
    # System ports (0-1023) - IANA assigned well-known ports
    *range(0, 1024),

    # Common application and development ports (1024-65535)
    # Databases
    1433,  # SQL Server
    1521,  # Oracle
    3306,  # MySQL
    5432,  # PostgreSQL
    6379,  # Redis
    9200,  # Elasticsearch
    9300,  # Elasticsearch cluster
    27017, # MongoDB

    # Message Queues & Streaming
    5672,  # RabbitMQ
    9092,  # Kafka
    15672, # RabbitMQ Management

    # Web Servers & Proxies
    1080,  # SOCKS proxy
    8080,  # HTTP alternate
    8443,  # HTTPS alternate
    8888,  # HTTP alternate
    9999,  # HTTP alternate

    # Development servers (common ranges)
    *range(3000, 3011),  # Node.js, React, etc.
    *range(4000, 4011),  # Ruby, Rails, etc.
    *range(5000, 5011),  # Flask, Django, etc.
    *range(8000, 8011),  # Django, HTTP alternates
    *range(9000, 9011),  # Various dev servers

    # Container & Orchestration
    2375, 2376, 2377,  # Docker
    6443,  # Kubernetes API
    2379, 2380,  # etcd
    10250, 10251, 10252, 10255,  # Kubernetes

    # Monitoring & Observability
    3000,  # Grafana (already in range above)
    9090,  # Prometheus
    9093,  # Alertmanager
    9100,  # Node Exporter
    4040,  # Spark UI

    # Application Servers
    8009,  # Tomcat AJP
    8005,  # Tomcat shutdown
    9080,  # WebSphere
    7001, 7002,  # WebLogic

    # Version Control & CI/CD
    8080,  # Jenkins (already listed)
    9000,  # SonarQube (already in range)
    3001,  # Gitiles (already in range)

    # Databases (additional)
    1521,  # Oracle (already listed)
    50000, # DB2
    7000, 7001,  # Cassandra
    8086,  # InfluxDB
    5984,  # CouchDB

    # Search & Analytics
    9200, 9300,  # Elasticsearch (already listed)
    8983,  # Solr

    # Caching
    11211, # Memcached
    6379,  # Redis (already listed)

    # Message Brokers
    61616, # ActiveMQ
    1883,  # MQTT

    # Web Hosting & Control Panels
    2082, 2083, 2086, 2087, 2095, 2096,  # cPanel

    # Zookeeper & Coordination
    2181,  # Zookeeper client
    2888,  # Zookeeper peer
    3888,  # Zookeeper leader election

    # Cache & Memory Stores
    11211, # Memcached

    # Build & CI/CD
    4567, 4568,  # Sinatra default ports
    8080,        # Jenkins (already listed)
    9000,        # SonarQube (already listed)

    # Hadoop Ecosystem
    50070, # HDFS NameNode
    50075, # HDFS DataNode
    8020,  # HDFS NameNode IPC
    8088,  # YARN ResourceManager

    # Other commonly blocked ranges
    # Avoid common ephemeral port ranges that might conflict
    32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775,  # Linux ephemeral start
    49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159,  # Windows ephemeral start
}

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"projects": {}, "used_ports": []}

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError:
        pass

def reset_config():
    """Reset configuration to default state"""
    default_config = {"projects": {}, "used_ports": []}
    save_config(default_config)
    return default_config

def project_name_to_number(name):
    """Convert project name to number using a=1, b=2, etc."""
    name = name.lower()
    result = ""
    for char in name:
        if char.isalpha():
            result += str(ord(char) - ord('a') + 1)

    if not result:
        return 0

    # If the result is too large for a valid port, use modulo to bring it into range
    port = int(result)
    if port > 65535:
        # Use modulo to get a number in the valid range, but ensure it's >= 1024
        port = (port % (65535 - 1024)) + 1024
    elif port < 1024:
        # If too small, add 1024 to get into user port range
        port += 1024

    return port

def is_valid_port(port):
    """Check if port is in valid range"""
    return 1024 <= port <= 65535

def is_port_available(port, config):
    """Check if port is available (not well-known, not used)"""
    return (port not in WELL_KNOWN_PORTS and
            port not in config.get("used_ports", []) and
            is_valid_port(port))

def find_available_port(base_port, config):
    """Find an available port starting from base_port"""
    port = base_port
    conflicts = []

    while not is_port_available(port, config):
        if port in WELL_KNOWN_PORTS:
            conflicts.append(f"Port {port} is a well-known port")
        elif port in config.get("used_ports", []):
            conflicts.append(f"Port {port} is already used")
        elif not is_valid_port(port):
            conflicts.append(f"Port {port} is out of valid range")

        # Try next port by adding a random digit
        port = int(str(port) + str((port % 10)))

        # Prevent infinite loop
        if port > 65535:
            port = base_port + 1000

        # Safety check to prevent infinite loop
        if len(conflicts) > 100:
            break

    return port, conflicts

def alfred_output(title, subtitle, arg=""):
    """Generate Alfred JSON output"""
    return {
        "items": [{
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
            "valid": True
        }]
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps(alfred_output("Port Roulette", "Usage: port <project-name> or port reset")))
        return

    project_name = sys.argv[1].strip()

    if not project_name:
        print(json.dumps(alfred_output("Port Roulette", "Please provide a project name or 'reset'")))
        return

    # Handle reset command
    if project_name.lower() == "reset":
        reset_config()
        print(json.dumps(alfred_output(
            "Database Reset",
            "Port database has been reset to default state",
            "reset"
        )))
        return

    config = load_config()

    # Check if project already has a port
    if project_name in config["projects"]:
        existing_port = config["projects"][project_name]
        print(json.dumps(alfred_output(
            f"Port {existing_port}",
            f"Existing port for '{project_name}'",
            str(existing_port)
        )))
        return

    # Generate new port
    base_port = project_name_to_number(project_name)

    if base_port == 0:
        print(json.dumps(alfred_output("Error", "Invalid project name - no letters found")))
        return

    port, conflicts = find_available_port(base_port, config)

    if not is_valid_port(port):
        print(json.dumps(alfred_output("Error", "Could not find a valid port")))
        return

    # Save the new port
    config["projects"][project_name] = port
    config["used_ports"].append(port)
    save_config(config)

    # Prepare output
    subtitle = f"New port for '{project_name}'"
    if conflicts:
        subtitle += f" (conflicts: {len(conflicts)})"

    print(json.dumps(alfred_output(
        f"Port {port}",
        subtitle,
        str(port)
    )))

if __name__ == "__main__":
    main()