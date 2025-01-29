# Contributing to Simple To-Do List CLI

## Introduction

Thank you for your interest in contributing to the Simple To-Do List CLI application! This guide provides comprehensive instructions for developers who want to contribute to the project. We welcome contributions that improve functionality, fix bugs, enhance documentation, or optimize performance.

Please read this document carefully before making any contributions.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We expect all participants to:

- Show respect and courtesy to others
- Use inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Enforcement

Violations of the code of conduct may result in temporary or permanent exclusion from project participation. Report violations to the project maintainers.

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR-USERNAME/simple-todo-cli.git
cd simple-todo-cli
```

### Development Environment Setup

1. Ensure Python 3.6+ is installed:
```bash
python --version
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Running Tests

Execute the test suite:
```bash
pytest tests/
```

Verify code coverage:
```bash
pytest --cov=src tests/
```

### Code Style Guidelines

- Follow PEP 8 style guide
- Use Black for code formatting
- Maximum line length: 80 characters
- Use meaningful variable and function names
- Include docstrings for all public functions/classes

## Development Workflow

### Creating Issues

- Search existing issues before creating new ones
- Use issue templates when available
- Provide clear reproduction steps for bugs
- Include system information where relevant
- Tag issues appropriately

### Branch Naming

Format: `type/description`

Types:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions/modifications
- `refactor/` - Code refactoring

Example: `feature/add-task-priority`

### Commit Messages

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```
feat(tasks): add task priority support

- Add priority field to Task class
- Update storage format to include priority
- Add priority sorting in list view

Closes #123
```

### Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Run all tests
4. Push to your fork
5. Submit a PR to `main`
6. Update PR based on review feedback

## Testing Requirements

### Unit Tests

- Required for all new features
- Minimum 90% coverage for new code
- Use pytest fixtures appropriately
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests

- Required for features affecting multiple components
- Test file operations with temporary files
- Verify CLI input/output behavior
- Test data persistence scenarios

### Code Coverage

- Maintain minimum 90% overall coverage
- No decrease in coverage allowed
- Generate coverage reports:
```bash
pytest --cov=src --cov-report=html tests/
```

## Code Quality

### Pylint Rules

- Maintain minimum score of 9.0/10
- Run pylint:
```bash
pylint src/
```

- No disabled checks without justification
- Follow error suppression guidelines

### Code Formatting

- Use Black with default settings:
```bash
black src/
```

- Run pre-commit hooks:
```bash
pre-commit run --all-files
```

### Documentation Standards

- Docstrings for all public APIs (Google style)
- Update README.md for user-facing changes
- Keep technical documentation current
- Include type hints (Python 3.6+)

Example docstring:
```python
def add_task(description: str, priority: int = 1) -> Task:
    """Adds a new task to the task list.

    Args:
        description: The task description text.
        priority: Task priority (1-5, 1 being highest).

    Returns:
        Task: The newly created task object.

    Raises:
        ValueError: If description is empty or priority is invalid.
    """
```

## Review Process

### Code Review Guidelines

Reviewers will check for:
- Functional correctness
- Test coverage
- Code style compliance
- Documentation completeness
- Security considerations
- Performance implications

### CI/CD Pipeline

All PRs must pass:
- Unit tests
- Integration tests
- Code coverage checks
- Pylint analysis
- Black formatting validation
- Security scans

### Merge Requirements

PRs can be merged when:
- All CI checks pass
- Required reviews are approved
- No unresolved conversations
- Up-to-date with main branch
- Commits are squashed if necessary

## Additional Resources

- [README.md](README.md) - Project overview and setup
- [SECURITY.md](SECURITY.md) - Security guidelines
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - CI pipeline configuration
- [infrastructure/config/pylintrc](infrastructure/config/pylintrc) - Pylint configuration

Thank you for contributing to Simple To-Do List CLI!