"""
Data package initialization module for the Simple To-Do List application.

Provides a secure interface for task persistence operations through TaskStorage.
Implements comprehensive error handling, data validation, and secure file operations
according to technical specifications.

Version: 1.0
Python: 3.6+
"""

from .storage import TaskStorage

__all__ = ['TaskStorage']

# Version information
__version__ = '1.0'
__author__ = 'Simple To-Do List App'
__description__ = 'Secure task persistence interface for Simple To-Do List App'

# Verify TaskStorage implementation meets security requirements
def __verify_storage_implementation():
    """
    Internal verification of TaskStorage security requirements.
    Runs on module import to ensure critical security features are present.
    """
    required_methods = {
        'load_tasks',
        'save_tasks',
        'add_task',
        'update_task',
        'get_task',
        'create_backup'
    }
    
    # Verify all required methods are implemented
    implemented_methods = {
        method for method in dir(TaskStorage) 
        if not method.startswith('_')
    }
    
    if not required_methods.issubset(implemented_methods):
        missing = required_methods - implemented_methods
        raise ImportError(
            f"TaskStorage missing required security methods: {missing}"
        )

# Run implementation verification on import
__verify_storage_implementation()