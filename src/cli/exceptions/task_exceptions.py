# Python 3.6+
"""
Custom exception classes for task-related errors in the Simple To-Do List application.
Provides specific error types with sanitized feedback for different task operation failures.
"""

# Error codes for task-related exceptions
ERROR_CODES = {
    'TASK_NOT_FOUND': 'E003',  # Invalid task number error code
    'TASK_LIMIT': 'E005'       # Storage limit reached error code
}

class TaskError(Exception):
    """
    Base exception class for all task-related errors.
    Provides consistent error handling and message formatting.
    
    Attributes:
        message (str): Sanitized error message for user display
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize the base task error with a sanitized error message.
        
        Args:
            message (str): Error message to display to user
        """
        # Sanitize message by stripping any system-specific information
        sanitized_message = str(message).replace('\n', ' ').strip()
        super().__init__(sanitized_message)
        self.message = sanitized_message

class TaskNotFoundError(TaskError):
    """
    Exception raised when attempting to access a non-existent task.
    Uses error code E003 for consistent error tracking.
    
    Attributes:
        message (str): User-friendly error message
        error_code (str): Standard error code E003
    """
    
    def __init__(self, task_id: int) -> None:
        """
        Initialize task not found error with task ID and error code E003.
        
        Args:
            task_id (int): ID of the task that was not found
        """
        self.error_code = ERROR_CODES['TASK_NOT_FOUND']
        message = f"Task {task_id} not found. Please enter a valid task number."
        super().__init__(message)

class TaskLimitError(TaskError):
    """
    Exception raised when task limit is exceeded.
    Uses error code E005 for consistent error tracking.
    
    Attributes:
        message (str): User-friendly error message
        error_code (str): Standard error code E005
    """
    
    def __init__(self, limit: int) -> None:
        """
        Initialize task limit error with maximum limit and error code E005.
        
        Args:
            limit (int): Maximum number of tasks allowed
        """
        self.error_code = ERROR_CODES['TASK_LIMIT']
        message = f"Task limit of {limit} tasks reached. Please remove some tasks before adding new ones."
        super().__init__(message)

class TaskValidationError(TaskError):
    """
    Exception raised when task validation fails.
    Provides specific validation error details with sanitized feedback.
    
    Attributes:
        message (str): Sanitized validation error message
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize task validation error with specific validation failure message.
        
        Args:
            message (str): Description of the validation failure
        """
        # Ensure validation messages don't expose system details
        sanitized_message = f"Task validation failed: {message}"
        super().__init__(sanitized_message)