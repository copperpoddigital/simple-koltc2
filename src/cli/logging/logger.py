"""
Logging configuration module for the Simple To-Do List App.

Implements secure error logging with file rotation and appropriate security measures.
Provides centralized logging functionality with proper file permissions and size limits.

Version: 1.0
"""

import logging
import os
from logging.handlers import RotatingFileHandler  # built-in
from typing import Optional

from ..config.settings import APP_SETTINGS, FILE_SETTINGS

# Logging configuration constants
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE_PATH = os.path.join(FILE_SETTINGS['DATA_DIR'], 'logs', 'todo.log')
MAX_LOG_SIZE = 1048576  # 1MB maximum log file size
BACKUP_COUNT = 1  # Keep one backup file

def setup_logging() -> logging.Logger:
    """
    Initializes and configures the application logger with appropriate handlers
    and security measures.

    Returns:
        logging.Logger: Configured logger instance with console and file handlers
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, mode=FILE_SETTINGS['FILE_PERMISSIONS'])
    
    # Set appropriate permissions on existing log directory
    os.chmod(log_dir, FILE_SETTINGS['FILE_PERMISSIONS'])

    # Create and configure logger
    logger = logging.getLogger(APP_SETTINGS['APP_NAME'])
    logger.setLevel(logging.DEBUG if APP_SETTINGS['DEBUG'] else logging.ERROR)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler with appropriate level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if APP_SETTINGS['DEBUG'] else logging.ERROR)

    # Create rotating file handler with secure permissions
    file_handler = RotatingFileHandler(
        filename=LOG_FILE_PATH,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        mode='a',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.ERROR)  # Always log errors to file

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Set secure permissions on log file
    if os.path.exists(LOG_FILE_PATH):
        os.chmod(LOG_FILE_PATH, FILE_SETTINGS['FILE_PERMISSIONS'])

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def get_logger() -> logging.Logger:
    """
    Returns a configured logger instance, creating it if necessary.
    Ensures singleton pattern for logger instance.

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(APP_SETTINGS['APP_NAME'])
    if not logger.handlers:
        logger = setup_logging()
    return logger