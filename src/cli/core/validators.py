"""
Input validation module for the Simple To-Do List application.

This module implements comprehensive validation functions for user inputs and task data,
ensuring data integrity and security through strict validation rules and sanitization.

Version: 1.0
"""

import re  # version: 3.6+
from datetime import datetime
from typing import Dict, Union

from ..types.custom_types import TaskId, TaskStatus, TaskDict
from ..exceptions.validation_exceptions import (
    ValidationError,
    TaskDescriptionValidationError,
    MenuOptionValidationError,
    TaskNumberValidationError
)
from ..constants.messages import ERROR_MESSAGES

# Constants for validation rules
TASK_DESCRIPTION_MAX_LENGTH = 200
TASK_DESCRIPTION_PATTERN = r'^[a-zA-Z0-9\s\.,!?-]*$'
MENU_OPTIONS = [1, 2, 3, 4]

def validate_task_description(description: str) -> bool:
    """
    Validates task description against length and character constraints.
    
    Args:
        description (str): Task description to validate
        
    Returns:
        bool: True if validation passes
        
    Raises:
        TaskDescriptionValidationError: If validation fails
    """
    if not description or description.isspace():
        raise TaskDescriptionValidationError(ERROR_MESSAGES['empty_description'])
    
    # Strip whitespace and validate length
    cleaned_description = description.strip()
    if len(cleaned_description) > TASK_DESCRIPTION_MAX_LENGTH:
        raise TaskDescriptionValidationError(ERROR_MESSAGES['description_too_long'])
        
    # Validate against allowed character pattern with timeout protection
    try:
        if not re.match(TASK_DESCRIPTION_PATTERN, cleaned_description, re.UNICODE):
            raise TaskDescriptionValidationError(ERROR_MESSAGES['invalid_chars'])
    except re.error:
        raise TaskDescriptionValidationError(ERROR_MESSAGES['system_error'])
        
    return True

def validate_menu_option(option: str) -> int:
    """
    Validates menu option input against allowed options.
    
    Args:
        option (str): Menu option input to validate
        
    Returns:
        int: Validated menu option number
        
    Raises:
        MenuOptionValidationError: If validation fails
    """
    try:
        option_num = int(option.strip())
        if option_num not in MENU_OPTIONS:
            raise MenuOptionValidationError(ERROR_MESSAGES['invalid_input'])
        return option_num
    except (ValueError, TypeError):
        raise MenuOptionValidationError(ERROR_MESSAGES['invalid_input'])

def validate_task_number(task_number: str, max_tasks: int) -> int:
    """
    Validates task number input against available task range.
    
    Args:
        task_number (str): Task number input to validate
        max_tasks (int): Maximum number of available tasks
        
    Returns:
        int: Validated task number
        
    Raises:
        TaskNumberValidationError: If validation fails
    """
    try:
        num = int(task_number.strip())
        if not 1 <= num <= max_tasks:
            raise TaskNumberValidationError(
                ERROR_MESSAGES['invalid_task_number'],
                max_tasks
            )
        return num
    except (ValueError, TypeError):
        raise TaskNumberValidationError(
            ERROR_MESSAGES['invalid_task_number'],
            max_tasks
        )

def validate_task_data(task_data: TaskDict) -> bool:
    """
    Validates complete task data structure with type and value checking.
    
    Args:
        task_data (TaskDict): Task data dictionary to validate
        
    Returns:
        bool: True if validation passes
        
    Raises:
        ValidationError: If validation fails
    """
    required_fields = {'id', 'description', 'status'}
    
    # Validate dictionary structure
    if not isinstance(task_data, dict):
        raise ValidationError(ERROR_MESSAGES['invalid_input'], "E004")
        
    # Check required fields
    if not all(field in task_data for field in required_fields):
        raise ValidationError(ERROR_MESSAGES['invalid_input'], "E005")
        
    # Validate field types and values
    try:
        # ID validation
        if not isinstance(task_data['id'], (int, str)):
            raise ValidationError(ERROR_MESSAGES['invalid_input'], "E006")
            
        # Description validation
        validate_task_description(task_data['description'])
        
        # Status validation
        if task_data['status'] not in ('pending', 'completed'):
            raise ValidationError(ERROR_MESSAGES['invalid_input'], "E007")
            
        # Timestamp validation if present
        for field in ('created', 'modified'):
            if field in task_data:
                if not isinstance(task_data[field], datetime):
                    raise ValidationError(ERROR_MESSAGES['invalid_input'], "E008")
                    
    except (KeyError, TypeError):
        raise ValidationError(ERROR_MESSAGES['invalid_input'], "E009")
        
    return True