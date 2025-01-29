"""
Main package initializer for the Simple To-Do List CLI application.
Exposes primary interfaces and version information with secure type checking.

Version: 1.0
Python: 3.6+
"""

import sys
from typing import Type, TypeVar, Optional  # version: 3.6+

from .interfaces.cli_interface import CLIInterface
from .core.task_manager import TaskManager
from .exceptions.task_exceptions import TaskError
from .exceptions.validation_exceptions import ValidationError
from .exceptions.storage_exceptions import StorageError

# Version and metadata information
__version__ = "1.0.0"
__author__ = "Simple To-Do List App Team"
__package_name__ = "simple-todo-cli"
__min_python_version__ = "3.6.0"

# Type variable for interface classes
T = TypeVar('T')

# Expose primary interfaces
__all__ = [
    'CLIInterface',
    'TaskManager',
    'TaskError',
    'ValidationError',
    'StorageError',
    'validate_environment',
    '__version__',
    '__author__',
    '__package_name__'
]

def validate_environment() -> bool:
    """
    Validates Python version and required dependencies at runtime.
    
    Returns:
        bool: True if environment is valid
        
    Raises:
        RuntimeError: If environment validation fails
    """
    # Validate Python version
    current_version = tuple(map(int, sys.version.split('.')[0:3]))
    required_version = tuple(map(int, __min_python_version__.split('.')))
    
    if current_version < required_version:
        raise RuntimeError(
            f"Python {__min_python_version__} or higher is required; "
            f"current version is {sys.version.split()[0]}"
        )

    # Validate required modules
    required_modules = {
        'typing': '3.6.0',
        'json': '3.6.0',
        'datetime': '3.6.0',
        'os': '3.6.0',
        'sys': '3.6.0',
        're': '3.6.0'
    }

    for module, version in required_modules.items():
        try:
            __import__(module)
        except ImportError:
            raise RuntimeError(f"Required module {module} (>= {version}) not found")

    # Validate interface class availability
    required_classes = {
        'CLIInterface': CLIInterface,
        'TaskManager': TaskManager
    }

    for class_name, class_type in required_classes.items():
        if not isinstance(class_type, type):
            raise RuntimeError(f"Required class {class_name} not properly initialized")

    return True

# Validate environment on import
validate_environment()