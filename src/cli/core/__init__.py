"""
Core module initialization for the Simple To-Do List application.

This module exports the main task management and validation components while maintaining
proper encapsulation and security measures. It provides a clean interface for accessing
core functionality according to technical specifications.

Version: 1.0
Python: 3.6+
"""

from .task_manager import TaskManager
from .validators import (
    validate_task_description,
    validate_menu_option,
    validate_task_number
)

# Define public interface
__all__ = [
    'TaskManager',
    'validate_task_description',
    'validate_menu_option', 
    'validate_task_number'
]

# Module metadata
__version__ = '1.0.0'
__author__ = 'Simple To-Do List App Team'

# Validate imports to ensure core components are available
if not all(component in globals() for component in __all__):
    raise ImportError("Core components failed to load properly")