"""
Entry point for the types module that re-exports all custom type definitions and type aliases.

This module provides centralized access to type hints for task data structures, menu options,
validation rules, and CLI interface components used throughout the application.

Version: 1.0
"""

from typing import Callable, Literal, List, TypeAlias  # Python 3.6+
from .custom_types import TaskDict, TaskId, TaskStatus, TaskList

# Re-export core task types
__all__ = [
    'TaskDict',
    'TaskId', 
    'TaskStatus',
    'TaskList',
    'MenuOption',
    'ValidationRule'
]

# Type definition for valid menu selections (1-4)
MenuOption = Literal[1, 2, 3, 4]

# Type definition for input validation functions
ValidationRule: TypeAlias = Callable[[str], bool]