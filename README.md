# drivedropbox-desktop
clg project

## Features

This application provides both Google Drive management and personal goal tracking capabilities:

### Google Drive Operations
- List files on Google Drive
- Show filesystem tree structure
- Upload files to Google Drive

### Personal Goal Management
- Add new personal goals
- View all current goals
- Remove goals by ID or description
- Goals are automatically saved locally and persist between sessions

## Usage

### Google Drive Commands

List files on Google Drive:
```bash
python main.py --list
```

Show filesystem tree:
```bash
python main.py --tree
```

Upload a file:
```bash
python main.py --upload
```

### Goal Management Commands

Add a new goal:
```bash
python main.py --add-goal "Learn Python programming"
```

List all your goals:
```bash
python main.py --list-goals
```

Remove a goal (by ID or exact description):
```bash
python main.py --remove-goal "a1b2c3d4"
python main.py --remove-goal "Learn Python programming"
```

### Goal Management Workflow Example

1. Add your first goal:
   ```bash
   python main.py --add-goal "Complete my Python project"
   ```

2. Add more goals:
   ```bash
   python main.py --add-goal "Exercise 3 times a week"
   python main.py --add-goal "Read one book per month"
   ```

3. View all your goals:
   ```bash
   python main.py --list-goals
   ```

4. Remove a completed goal:
   ```bash
   python main.py --remove-goal "Complete my Python project"
   ```

## Goal Data Storage

Goals are stored locally in a `goals.json` file in the same directory as the application. This file is automatically created when you add your first goal and is updated whenever you make changes to your goals.

## Error Handling

The application includes error handling for common scenarios:
- Empty goal descriptions
- File read/write errors
- Invalid goal identifiers
- Network issues with Google Drive operations
