"""
Logging package initialization module for the Simple To-Do List App.

Provides centralized access to secure logging functionality with appropriate error handling,
audit trails, and configurable log rotation. Implements security-focused logging with
generic error messages and strict file permissions.

Version: 1.0
"""

from .logger import setup_logging as setup_logger  # version: 1.0
from .logger import get_logger  # version: 1.0

# Re-export core logging functionality
__all__ = ['setup_logger', 'get_logger']

# Initialize package-level logger with secure defaults
logger = get_logger()