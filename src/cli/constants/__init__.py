"""
Constants module for the Simple To-Do List application.
Centralizes all constant values used throughout the application including messages,
symbols, UI elements, and validation parameters.

Version: 1.0
"""

# Import all message constants
from .messages import (
    WELCOME_MESSAGE,
    MAIN_MENU_OPTIONS,
    INPUT_PROMPTS,
    SUCCESS_MESSAGES,
    ERROR_MESSAGES,
    INFO_MESSAGES,
    HELP_MESSAGES,
    GUIDELINES
)

# Import all symbol constants
from .symbols import (
    NAVIGATION_SYMBOLS,
    STATUS_SYMBOLS,
    ACTION_SYMBOLS,
    BORDER_SYMBOLS,
    MENU_SYMBOLS
)

# Application-wide constants
APP_VERSION = "1.0"

# Input validation constants
MAX_TASK_LENGTH = 200  # Maximum characters allowed in task description
MAX_TASKS = 1000      # Maximum number of tasks allowed in the list

# Display formatting constants
SCREEN_WIDTH = 80     # Standard screen width for CLI display

# Export all constants for application-wide use
__all__ = [
    # Message constants
    'WELCOME_MESSAGE',
    'MAIN_MENU_OPTIONS',
    'INPUT_PROMPTS',
    'SUCCESS_MESSAGES',
    'ERROR_MESSAGES',
    'INFO_MESSAGES',
    'HELP_MESSAGES',
    'GUIDELINES',
    
    # Symbol constants
    'NAVIGATION_SYMBOLS',
    'STATUS_SYMBOLS',
    'ACTION_SYMBOLS',
    'BORDER_SYMBOLS',
    'MENU_SYMBOLS',
    
    # Application constants
    'APP_VERSION',
    'MAX_TASK_LENGTH',
    'MAX_TASKS',
    'SCREEN_WIDTH'
]