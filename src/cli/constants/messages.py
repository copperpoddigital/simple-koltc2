"""
Constants module containing all user-facing messages used throughout the Simple To-Do List application.
Centralizes text content to maintain consistency and enable easy updates.

Version: 1.0
"""

from typing import Dict  # Python 3.6+

# Success messages with status indicators
SUCCESS_MESSAGES: Dict[str, str] = {
    'task_added': '[+] Task added successfully',
    'task_completed': '[x] Task marked as complete',
    'backup_created': '[i] Backup created successfully',
    'file_saved': '[i] Changes saved successfully',
    'operation_complete': '[i] Operation completed successfully'
}

# Error messages with clear instructions and security considerations
ERROR_MESSAGES: Dict[str, str] = {
    'invalid_input': '[!] Invalid input. Please try again.',
    'invalid_task_number': '[!] Invalid task number. Please enter a valid number.',
    'file_access_error': '[!] Unable to access task file. Please check permissions.',
    'empty_description': '[!] Task description cannot be empty.',
    'description_too_long': '[!] Task description must be less than 200 characters.',
    'invalid_chars': '[!] Task description contains invalid characters.',
    'system_error': '[!] An error occurred. Please try again.',
    'backup_failed': '[!] Backup creation failed.',
    'task_not_found': '[!] Task not found.',
    'list_full': '[!] Task list is full (maximum 1000 tasks).'
}

# Informational messages for user guidance and status updates
INFO_MESSAGES: Dict[str, str] = {
    'welcome': '=== Welcome to Simple To-Do List App ===',
    'exit': '=== Thank you for using Simple To-Do List App ===',
    'no_tasks': '[i] No tasks found.',
    'press_enter': 'Press [Enter] to continue...',
    'task_count': '[i] Total Tasks: {}, Completed: {}, Pending: {}',
    'help_available': '[?] Press H for help',
    'loading': '[i] Loading tasks...',
    'saving': '[i] Saving changes...',
    'confirm_exit': '[i] Press [Enter] again to exit'
}

# Menu-related messages with standardized layout elements
MENU_MESSAGES: Dict[str, str] = {
    'main_title': '=== Simple To-Do List App ===',
    'add_task': '1. Add Task',
    'view_tasks': '2. View Tasks', 
    'complete_task': '3. Mark Task as Complete',
    'exit': '4. Exit',
    'choice_prompt': 'Enter your choice (1-4): ',
    'add_task_prompt': 'Enter task description: ',
    'complete_task_prompt': 'Enter task number to complete: ',
    'task_format': '{:3d}. [{}] {}',  # Format: number. [status] description
    'divider': '-' * 80,
    'header': '| {:^76} |',  # Centered text with borders
    'footer': '=' * 80
}