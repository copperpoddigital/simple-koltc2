"""
Utility module for handling and validating user input in the Simple To-Do List CLI application.
Provides secure input validation, sanitization, and standardized input collection with type safety.

Version: 1.0
"""

import re  # version: 3.6+
from typing import Union  # version: 3.6+

from ..constants.messages import ERROR_MESSAGES, MENU_MESSAGES
from ..exceptions.validation_exceptions import (
    ValidationError,
    TaskDescriptionValidationError,
    MenuOptionValidationError,
    TaskNumberValidationError
)
from ..types.custom_types import TaskId

# Constants for input validation
TASK_DESCRIPTION_MAX_LENGTH = 200
VALID_MENU_OPTIONS = [1, 2, 3, 4]
TASK_DESCRIPTION_PATTERN = r'^[a-zA-Z0-9\s\.,!?-]*$'

def get_menu_option() -> int:
    """
    Gets and validates user input for menu selection.
    
    Returns:
        int: Validated menu option number (1-4)
        
    Raises:
        MenuOptionValidationError: If input is invalid
    """
    try:
        option = input(MENU_MESSAGES['choice_prompt']).strip()
        validate_menu_option(option)
        return int(option)
    except ValidationError as e:
        print(e.message)
        return get_menu_option()

def get_task_description() -> str:
    """
    Gets and validates user input for task description with security checks.
    
    Returns:
        str: Validated and sanitized task description
        
    Raises:
        TaskDescriptionValidationError: If description is invalid
    """
    description = input(MENU_MESSAGES['add_task_prompt']).strip()
    
    try:
        validate_task_description(description)
        return description
    except ValidationError as e:
        print(e.message)
        return get_task_description()

def get_task_number(max_tasks: int) -> TaskId:
    """
    Gets and validates user input for task selection.
    
    Args:
        max_tasks (int): Maximum number of available tasks
        
    Returns:
        TaskId: Validated task number
        
    Raises:
        TaskNumberValidationError: If task number is invalid
    """
    try:
        number = input(MENU_MESSAGES['complete_task_prompt']).strip()
        validate_task_number(number, max_tasks)
        return int(number)
    except ValidationError as e:
        print(e.message)
        return get_task_number(max_tasks)

def validate_menu_option(option: str) -> bool:
    """
    Validates if input is a valid menu option.
    
    Args:
        option (str): User input for menu selection
        
    Returns:
        bool: True if valid
        
    Raises:
        MenuOptionValidationError: If option is invalid
    """
    if not option.isdigit():
        raise MenuOptionValidationError(ERROR_MESSAGES['invalid_input'])
    
    option_num = int(option)
    if option_num not in VALID_MENU_OPTIONS:
        raise MenuOptionValidationError(ERROR_MESSAGES['invalid_input'])
    
    return True

def validate_task_description(description: str) -> bool:
    """
    Validates task description format and content with security checks.
    
    Args:
        description (str): Task description to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        TaskDescriptionValidationError: If description is invalid
    """
    if not description or description.isspace():
        raise TaskDescriptionValidationError(ERROR_MESSAGES['empty_description'])
    
    if len(description) > TASK_DESCRIPTION_MAX_LENGTH:
        raise TaskDescriptionValidationError(ERROR_MESSAGES['description_too_long'])
    
    if not re.match(TASK_DESCRIPTION_PATTERN, description):
        raise TaskDescriptionValidationError(ERROR_MESSAGES['invalid_chars'])
    
    return True

def validate_task_number(number: str, max_tasks: int) -> bool:
    """
    Validates task number input with range checking.
    
    Args:
        number (str): Task number input to validate
        max_tasks (int): Maximum number of available tasks
        
    Returns:
        bool: True if valid
        
    Raises:
        TaskNumberValidationError: If number is invalid
    """
    if not number.isdigit():
        raise TaskNumberValidationError(ERROR_MESSAGES['invalid_task_number'], max_tasks)
    
    task_num = int(number)
    if task_num < 1 or task_num > max_tasks:
        raise TaskNumberValidationError(ERROR_MESSAGES['invalid_task_number'], max_tasks)
    
    return True