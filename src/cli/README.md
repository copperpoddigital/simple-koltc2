# Simple To-Do List CLI

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/todo-cli/actions)

A lightweight command-line task management application for efficient task tracking and organization.

## Features

- Task Creation - Simple text-based task entry
- Task Viewing - Clean numbered list display
- Status Updates - Easy completion marking
- Data Persistence - Reliable local file storage

## Requirements

### System Requirements
- Python 3.6 or higher
- 50MB available memory
- Read/write access to home directory

### Dependencies
All dependencies are listed in `requirements.txt`. Core dependencies include:
```
python>=3.6.0
```

## Installation

1. Ensure Python 3.6+ is installed:
```bash
python --version
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment (optional):
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration as needed
nano .env
```

## Usage

Launch the application:
```bash
python main.py
```

### Menu Options

1. Add Task (Option 1)
   ```
   Enter choice: 1
   Enter task description: Buy groceries
   ```

2. View Tasks (Option 2)
   ```
   Enter choice: 2
   Current Tasks:
   1. [ ] Buy groceries
   2. [x] Call dentist
   ```

3. Mark Task as Complete (Option 3)
   ```
   Enter choice: 3
   Enter task number: 1
   Task marked as complete!
   ```

4. Exit (Option 4)
   ```
   Enter choice: 4
   Goodbye!
   ```

### Navigation Tips
- Enter numbers 1-4 to select menu options
- Press Enter to confirm selections
- Press Ctrl+C to exit at any time

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-cli.git
cd todo-cli
```

2. Create development virtual environment:
```bash
python -m venv venv-dev
source venv-dev/bin/activate  # Unix/MacOS
venv-dev\Scripts\activate     # Windows
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use meaningful variable names
- Include docstrings for all functions
- Maintain 80 character line length
- Add comments for complex logic

### Testing

Run tests:
```bash
pytest tests/
```

Generate coverage report:
```bash
pytest --cov=src tests/
```

### Pull Request Process

1. Create feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Push changes and create PR:
```bash
git push origin feature/your-feature-name
```

4. Ensure CI passes and request review

## Error Codes

| Code | Description | Recovery Action |
|------|-------------|----------------|
| E001 | File access denied | Check user permissions |
| E002 | Corrupt data file | Restore from backup |
| E003 | Invalid task number | Re-enter valid number |
| E004 | Memory allocation error | Restart application |
| E005 | Storage limit reached | Remove completed tasks |

### Error Categories

- File Operations (E001-E002)
  - Related to file access and data integrity
- Input Validation (E003)
  - Related to user input processing
- System Errors (E004-E005)
  - Related to resource management

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Python community for excellent documentation
- Contributors who have helped improve the project