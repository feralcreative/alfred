# <img src="./images/icons/icon-port-roulette.svg" width="32" height="32" alt="Port Roulette"> Port Roulette - Alfred Workflow

Generate unique port numbers for development projects with intelligent conflict avoidance.

## Overview

Port Roulette is an Alfred workflow that helps developers quickly generate and manage unique port numbers for their projects. It converts project names into port numbers using a simple algorithm, avoids well-known ports and previously used ports, and maintains a persistent configuration to ensure no conflicts.

## Features

- **Smart Port Generation**: Converts project names to numbers (a=1, b=2, etc.) to create memorable port assignments
- **Conflict Avoidance**: Automatically avoids well-known ports (0-1023) and common application ports
- **Persistent Memory**: Remembers previously assigned ports to prevent conflicts
- **Automatic Fallback**: If the calculated port is taken, automatically finds the next available port
- **Instant Clipboard**: Selected port numbers are automatically copied to clipboard
- **Configurable Storage**: Config file location can be easily customized
- **Database Reset**: Reset functionality to clear all stored port assignments

## Installation

1. Download the `port-roulette.alfredworkflow` file
2. Double-click to install in Alfred
3. Ensure Python 3 is available in your system PATH

## Usage

### Basic Usage

```bash
port <project-name>
```

### Examples

```bash
port pge          # Generates port for "pge" project (likely 1675: p=16, g=7, e=5)
port myapp        # Generates port for "myapp" project
port frontend     # Generates port for "frontend" project
port reset        # Reset the port database to default state
```

### First Time vs. Subsequent Calls

- **First time**: Calculates new port based on project name, saves to config
- **Subsequent times**: Returns the same port number that was previously assigned

## How It Works

1. **Name to Number Conversion**: Each letter in the project name is converted to its position in the alphabet (a=1, b=2, c=3, etc.)
2. **Port Calculation**: The numbers are concatenated to form a base port number
3. **Validation**: Checks if the port is:
   - In valid range (1024-65535)
   - Not a well-known port
   - Not previously used
4. **Conflict Resolution**: If conflicts exist, appends digits until an available port is found
5. **Persistence**: Saves the assignment to `~/.port-roulette-config.json`

## Configuration

The workflow maintains its state in `~/.port-roulette-config.json`:

```json
{
  "projects": {
    "pge": 1675,
    "myapp": 13125116
  },
  "used_ports": [1675, 13125116]
}
```

## Well-Known Ports Avoided

The workflow avoids a comprehensive list of ports including:

### System Ports (0-1023)

All IANA-assigned well-known ports including HTTP (80), HTTPS (443), SSH (22), FTP (21), etc.

### Common Application Ports

- **Databases**: MySQL (3306), PostgreSQL (5432), MongoDB (27017), Redis (6379)
- **Development Servers**: 3000-3010, 4000-4010, 5000-5010, 8000-8010, 9000-9010
- **Container/Orchestration**: Docker (2375-2377), Kubernetes (6443), etcd (2379-2380)
- **Monitoring**: Prometheus (9090), Grafana (3000), Elasticsearch (9200)
- **Message Queues**: RabbitMQ (5672), Kafka (9092)
- **And many more...**

## Requirements

- Alfred 5+ with Powerpack
- Python 3.x
- macOS

## Troubleshooting

### Port Not Generated

- Ensure Python 3 is installed and accessible via `python3` command
- Check that the project name contains at least one letter

### Configuration Issues

- The config file is stored at `~/www/_vscode/port-roulette-config.json` by default
- Use `port reset` command to reset all port assignments
- Ensure write permissions to the config directory

## Configuration

### Config File Location

The workflow stores port assignments in a JSON configuration file. By default, this is located at:

```
~/www/_vscode/port-roulette-config.json
```

### Customizing Config Location

To change the config file location, edit the `CONFIG_DIR` variable in `port-roulette.py`:

```python
# Configuration file path - can be customized by changing this line
# Default: ~/www/_vscode/port-roulette-config.json
# Alternative: ~/.port-roulette-config.json (original location)
CONFIG_DIR = os.path.expanduser("~/www/_vscode")
```

Common alternatives:
- `~/.port-roulette-config.json` (original location)
- `~/.config/port-roulette/config.json`
- `~/Documents/port-roulette-config.json`

### Reset Database

To reset all port assignments and start fresh:

```bash
port reset
```

This will:
- Clear all project-to-port mappings
- Reset the used ports list
- Restore the database to its default empty state

### Manual Reset

Alternatively, you can manually delete the config file:

```bash
rm ~/www/_vscode/port-roulette-config.json
```

## Development

### File Structure

```text
port-roulette/
├── port-roulette.py              # Main Python script
├── info.plist                    # Alfred workflow configuration
├── port-roulette.alfredworkflow  # Packaged workflow file
├── package.sh                    # Build script for packaging
└── README.md                     # This file
```

### Building the Workflow

To package the workflow for distribution:

```bash
./package.sh
```

Alternatively, you can manually create the package:

1. Select all files in the port-roulette directory
2. Right-click and choose "Compress" to create a .zip file
3. Rename the .zip file to .alfredworkflow

## License

MIT License - feel free to modify and distribute.

## Contributing

Issues and pull requests welcome at [https://github.com/feralcreative/alfred](https://github.com/feralcreative/alfred).
