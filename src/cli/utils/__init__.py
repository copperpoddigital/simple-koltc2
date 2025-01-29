"""
Initialization module for the utils package that exports utility functions for file operations,
input handling, and output formatting. Provides a centralized access point for all utility
functions used throughout the To-Do List application.

Version: 1.0
Python: 3.6+
"""

# File operation utilities
from .file_utils import (
    ensure_directory_exists,
    read_json_file,
    write_json_file,
    create_backup,
    validate_file_path
)

# Input handling utilities
from .input_utils import (
    get_menu_input,
    get_task_description,
    get_task_number,
    sanitize_input
)

# Output formatting utilities
from .output_utils import (
    clear_screen,
    print_header,
    print_menu,
    format_task,
    print_task_list,
    print_message,
    print_help
)

__all__ = [
    # File operations
    'ensure_directory_exists',
    'read_json_file',
    'write_json_file',
    'create_backup',
    'validate_file_path',
    
    # Input handling
    'get_menu_input',
    'get_task_description',
    'get_task_number',
    'sanitize_input',
    
    # Output formatting
    'clear_screen',
    'print_header',
    'print_menu',
    'format_task',
    'print_task_list',
    'print_message',
    'print_help'
]

# Package metadata
__version__ = '1.0'
__author__ = 'Simple To-Do List App'
__description__ = 'Utility functions for the Simple To-Do List CLI application'