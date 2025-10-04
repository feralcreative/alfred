# <img src="./icon.png" width="32" height="32" alt="Augment Code Tasks"> Augment Code Workflow

This Alfred workflow provides productivity tools for development, including task entry creation and process management.

## Installation

1. Double-click the `augment-code-tasks.alfredworkflow` file
2. Alfred will prompt you to install the workflow
3. Click "Import" to add it to your Alfred workflows

## Commands

### 1. Create Task Entry (`au`)

1. Toggle Alfred (⌥ + Space on my Mac)
2. Type `au` followed by your task name
3. Press Enter
4. The formatted task entry will be automatically pasted into the active document

**Example:**

Type: `au Create user authentication system`

Output (pasted into active document):

```
-[ ] NAME:Create user authentication system DESCRIPTION:
```

### 2. Kill Process on Port (`killport`)

1. Toggle Alfred (⌥ + Space on my Mac)
2. Type `killport` followed by the port number
3. Press Enter
4. All processes using that port will be killed

**Example:**

Type: `killport 3000`

Result: Kills all processes running on port 3000 using the command:
```bash
lsof -ti:3000 | xargs kill -9
```

## Task Entry Format

The workflow generates task entries in this format:

```
-[ ] NAME:Task name DESCRIPTION: Description of the task goes here.
```

This format is compatible with the task management system used by Augment Code agent.

## Files

- `info.plist` - Alfred workflow configuration
- `icon.png` - Workflow icon
- `augment-code-tasks.alfredworkflow` - Packaged workflow file for installation
