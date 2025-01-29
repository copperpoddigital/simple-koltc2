"""
Custom validation exceptions for the Simple To-Do List application.

This module defines exception classes for various validation failures in the application,
providing specific error messages and error codes for different validation scenarios.

Version: 1.0
"""

from ..types.custom_types import TaskId, TaskStatus

class ValidationError(Exception):
    """Base exception class for all validation-related errors in the application."""
    
    def __init__(self, message: str, error_code: str) -> None:
        """
        Initialize validation error with message and error code.
        
        Args:
            message (str): Detailed error message
            error_code (str): Unique error code identifier
        """
        self.message = f"[{error_code}] {message}"
        self.error_code = error_code
        super().__init__(self.message)


class TaskDescriptionValidationError(ValidationError):
    """Exception raised when task description validation fails."""
    
    def __init__(self, message: str) -> None:
        """
        Initialize task description validation error.
        
        Args:
            message (str): Specific validation error message
        """
        validation_rules = (
            "Task description must be between 1 and 200 characters and contain "
            "only alphanumeric characters and basic punctuation."
        )
        recovery_action = "Please revise your task description and try again."
        full_message = f"{message}\n{validation_rules}\n{recovery_action}"
        super().__init__(full_message, "E001")


class MenuOptionValidationError(ValidationError):
    """Exception raised when menu option validation fails."""
    
    def __init__(self, message: str) -> None:
        """
        Initialize menu option validation error.
        
        Args:
            message (str): Specific validation error message
        """
        validation_rules = "Menu options must be a number between 1 and 4."
        recovery_action = "Please enter a valid menu option number."
        full_message = f"{message}\n{validation_rules}\n{recovery_action}"
        super().__init__(full_message, "E002")


class TaskNumberValidationError(ValidationError):
    """Exception raised when task number validation fails."""
    
    def __init__(self, message: str, max_tasks: int) -> None:
        """
        Initialize task number validation error.
        
        Args:
            message (str): Specific validation error message
            max_tasks (int): Maximum number of available tasks
        """
        self.max_tasks = max_tasks
        validation_rules = f"Task number must be between 1 and {max_tasks}."
        recovery_action = "Please enter a valid task number from the list."
        full_message = f"{message}\n{validation_rules}\n{recovery_action}"
        super().__init__(full_message, "E003")