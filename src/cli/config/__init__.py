"""
Configuration module initialization for the Simple To-Do List App.
Provides centralized access to all application settings by re-exporting
configuration values from the settings module.

This module serves as the main configuration entry point, ensuring type safety
and proper initialization of all settings required by the application.

Version: 1.0
"""

from typing import Dict, Any

from .settings import (
    DEBUG,
    DATA_DIR,
    TASKS_FILE,
    BACKUP_FILE,
    FILE_PERMISSIONS,
    MAX_TASKS,
    MAX_DESCRIPTION_LENGTH,
    OPERATION_TIMEOUT,
    MAX_FILE_SIZE,
    LOG_LEVEL,
    get_config,
    load_config,
    validate_config
)

# Application settings with core configuration values
APP_SETTINGS: Dict[str, Any] = {
    'APP_NAME': 'Simple To-Do List App',
    'APP_VERSION': '1.0',
    'DEBUG': DEBUG
}

# File-related settings for data storage and permissions
FILE_SETTINGS: Dict[str, Any] = {
    'DATA_DIR': DATA_DIR,
    'TASKS_FILE': TASKS_FILE,
    'BACKUP_FILE': BACKUP_FILE,
    'FILE_PERMISSIONS': FILE_PERMISSIONS
}

# Task-specific settings for validation and limits
TASK_SETTINGS: Dict[str, Any] = {
    'MAX_TASKS': MAX_TASKS,
    'MAX_DESCRIPTION_LENGTH': MAX_DESCRIPTION_LENGTH,
    'ALLOWED_CHARS': set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?()-_')
}

# Performance-related settings for operation limits
PERFORMANCE_SETTINGS: Dict[str, Any] = {
    'OPERATION_TIMEOUT': OPERATION_TIMEOUT,
    'MAX_FILE_SIZE': MAX_FILE_SIZE
}

# Re-export configuration management functions
__all__ = [
    'APP_SETTINGS',
    'FILE_SETTINGS',
    'TASK_SETTINGS',
    'PERFORMANCE_SETTINGS',
    'get_config',
    'load_config',
    'validate_config'
]