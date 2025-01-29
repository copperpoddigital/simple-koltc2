# Simple To-Do List CLI

[![Build Status](https://github.com/username/todo-cli/workflows/CI/badge.svg)](https://github.com/username/todo-cli/actions)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/username/todo-cli/releases)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A lightweight command-line task management solution designed for efficient task tracking with minimal complexity. This application provides a straightforward way to manage your daily tasks through a clean, text-based interface.

## Features

- ✏️ **Task Creation** - Quick text-based task entry
- 📋 **Task Viewing** - Clear numbered list display
- ✅ **Status Updates** - Simple completion marking
- 💾 **Data Persistence** - Reliable local file storage
- 🖥️ **Simple Interface** - Intuitive command-line based
- 🔄 **Cross-platform** - Works seamlessly on Windows, Linux, and MacOS

## Requirements

- Python 3.6 or higher
- Less than 1MB disk space
- Less than 50MB RAM
- Any operating system with Python support

## Installation

1. Ensure Python 3.6+ is installed:
```bash
python --version
```

2. Install the package:
```bash
pip install simple-todo-cli
```

3. Verify installation:
```bash
todo --version
```

## Usage

Basic commands:

```bash
# Add a new task
todo add "Buy groceries"

# View all tasks
todo list

# Mark task as complete
todo complete 1

# Exit application
todo exit
```

Common operations:

```bash
# Add task with more details
todo add "Call dentist" 

# View only pending tasks
todo list --pending

# View only completed tasks
todo list --completed
```

## Documentation

- [Detailed CLI Guide](src/cli/README.md) - Advanced usage and commands
- [API Documentation](docs/API.md) - For developers and integrators
- [Configuration Guide](docs/CONFIG.md) - Customization options

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Submit a Pull Request

## Security

For security concerns, please review our [Security Policy](SECURITY.md).

To report a vulnerability, please follow the process outlined in our security documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Simple To-Do List CLI Contributors