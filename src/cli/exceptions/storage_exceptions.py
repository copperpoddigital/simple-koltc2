"""
Custom exception classes for handling storage-related errors in the Simple To-Do List application.

This module provides specific exception types for various storage-related issues including
file access problems and data corruption scenarios. Each exception type includes a specific
error code and sanitized error messages that are user-friendly while maintaining security.

Version: 1.0
Python: 3.6+
"""


class StorageError(Exception):
    """
    Base exception class for all storage-related errors in the application.
    
    Provides a foundation for more specific storage error types with standardized
    message handling and error code support.
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize the base storage error with a sanitized message.
        
        Args:
            message (str): A user-friendly error message describing the issue
        """
        super().__init__(message)
        self.error_code = None  # Base class has no specific error code


class FileAccessError(StorageError):
    """
    Exception raised when file access or permission issues occur.
    
    Used for scenarios such as:
    - Insufficient permissions to read/write files
    - File not found
    - File system access issues
    
    Error code: E001
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize file access error with error code E001.
        
        Args:
            message (str): A user-friendly error message describing the access issue
        """
        super().__init__(message)
        self.error_code = 'E001'  # Specific error code for file access issues


class DataCorruptionError(StorageError):
    """
    Exception raised when data file corruption is detected.
    
    Used for scenarios such as:
    - Invalid JSON format
    - Missing required data fields
    - Inconsistent data structure
    
    Error code: E002
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize data corruption error with error code E002.
        
        Args:
            message (str): A user-friendly error message describing the corruption issue
        """
        super().__init__(message)
        self.error_code = 'E002'  # Specific error code for data corruption issues