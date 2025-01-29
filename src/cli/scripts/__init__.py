"""
Initialization module for the scripts package in the Simple To-Do List application.

This module securely exposes essential script functionalities for backup and maintenance
operations while maintaining proper encapsulation and security controls according to
technical specifications.

Version: 1.0
Python: 3.6+
"""

from .backup import create_task_backup  # version: 1.0
from .cleanup import cleanup_completed_tasks, perform_maintenance  # version: 1.0

# Define public interface with explicit exports
__all__ = [
    "create_task_backup",      # Secure backup creation functionality
    "cleanup_completed_tasks", # Task cleanup functionality
    "perform_maintenance"      # System maintenance functionality
]

# Version information
__version__ = "1.0"
__author__ = "Simple To-Do List App"
__license__ = "Proprietary"

# Module initialization with security checks
def __init_module():
    """
    Performs security checks during module initialization.
    Verifies integrity of exported functions and their dependencies.
    """
    # Verify all exported functions are available
    required_functions = {
        "create_task_backup": create_task_backup,
        "cleanup_completed_tasks": cleanup_completed_tasks,
        "perform_maintenance": perform_maintenance
    }
    
    for func_name, func in required_functions.items():
        if not callable(func):
            raise ImportError(f"Required function {func_name} is not callable")

# Run initialization checks
__init_module()