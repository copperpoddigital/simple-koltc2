"""
Centralized exception exports for the Simple To-Do List application.

This module provides a single import point for all custom exceptions used throughout
the application, ensuring consistent error handling and standardized error codes.

Error Code Reference:
- E001: File access and permission issues
- E002: Data corruption issues
- E003: Invalid task number/not found
- E004: Input validation failures
- E005: Task limit exceeded

Version: 1.0
Python: 3.6+
"""

from .storage_exceptions import (
    StorageError,
    FileAccessError,
    DataCorruptionError
)

from .task_exceptions import (
    TaskError,
    TaskNotFoundError,
    TaskLimitError,
    TaskValidationError
)

from .validation_exceptions import (
    ValidationError,
    TaskDescriptionValidationError,
    MenuOptionValidationError,
    TaskNumberValidationError
)

# Export all exception classes for application-wide use
__all__ = [
    # Storage Exceptions (E001-E002)
    'StorageError',          # Base storage exception
    'FileAccessError',       # E001: File access issues
    'DataCorruptionError',   # E002: Data corruption

    # Task Exceptions (E003, E005)
    'TaskError',            # Base task exception
    'TaskNotFoundError',    # E003: Task not found
    'TaskLimitError',       # E005: Task limit exceeded
    'TaskValidationError',  # Task-specific validation

    # Validation Exceptions (E004)
    'ValidationError',                 # Base validation exception
    'TaskDescriptionValidationError',  # E004: Task description validation
    'MenuOptionValidationError',       # E004: Menu option validation
    'TaskNumberValidationError'        # E004: Task number validation
]