"""
Central configuration module for the Simple To-Do List App.
Manages application settings, environment variables, and constants with secure defaults.

This module implements comprehensive configuration management with type safety,
secure defaults, and validation for all settings. It handles file permissions,
performance limits, and security configurations.

Version: 1.0
"""

import os
from os import path
from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv  # version: 0.19.0

from ..constants.messages import SUCCESS_MESSAGES, ERROR_MESSAGES, INFO_MESSAGES
from ..types.custom_types import TaskDict, TaskList, ConfigDict, MetadataDict

# Load environment variables with secure defaults
DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
DATA_DIR: str = os.getenv('DATA_DIR', os.path.expanduser('~/.todo/data'))
TASKS_FILE: str = os.getenv('TASKS_FILE', 'tasks.json')
BACKUP_FILE: str = os.getenv('BACKUP_FILE', 'tasks.json.bak')
FILE_PERMISSIONS: int = int(os.getenv('FILE_PERMISSIONS', '600'), 8)
MAX_TASKS: int = int(os.getenv('MAX_TASKS', '1000'))
MAX_DESCRIPTION_LENGTH: int = int(os.getenv('MAX_DESCRIPTION_LENGTH', '200'))
OPERATION_TIMEOUT: int = int(os.getenv('OPERATION_TIMEOUT', '1000'))  # milliseconds
MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '1048576'))  # 1MB
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'ERROR')

# Configuration cache for performance optimization
CONFIG_CACHE: Optional[Dict[str, Any]] = None

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Performs comprehensive validation of configuration values against security
    and performance requirements.

    Args:
        config: Dictionary containing configuration settings to validate

    Returns:
        bool: True if configuration is valid

    Raises:
        ValueError: If any configuration value is invalid with detailed message
    """
    required_keys = {
        'DEBUG': bool,
        'DATA_DIR': str,
        'TASKS_FILE': str,
        'BACKUP_FILE': str,
        'FILE_PERMISSIONS': int,
        'MAX_TASKS': int,
        'MAX_DESCRIPTION_LENGTH': int,
        'OPERATION_TIMEOUT': int,
        'MAX_FILE_SIZE': int,
        'LOG_LEVEL': str
    }

    # Verify all required keys exist with correct types
    for key, expected_type in required_keys.items():
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
        if not isinstance(config[key], expected_type):
            raise ValueError(f"Invalid type for {key}: expected {expected_type}, got {type(config[key])}")

    # Validate numeric ranges
    if not (0 <= config['FILE_PERMISSIONS'] <= 0o777):
        raise ValueError("FILE_PERMISSIONS must be a valid octal between 000 and 777")
    
    if not (1 <= config['MAX_TASKS'] <= 10000):
        raise ValueError("MAX_TASKS must be between 1 and 10000")
    
    if not (1 <= config['MAX_DESCRIPTION_LENGTH'] <= 1000):
        raise ValueError("MAX_DESCRIPTION_LENGTH must be between 1 and 1000")
    
    if not (100 <= config['OPERATION_TIMEOUT'] <= 10000):
        raise ValueError("OPERATION_TIMEOUT must be between 100 and 10000 milliseconds")
    
    if not (1024 <= config['MAX_FILE_SIZE'] <= 10485760):  # 1KB to 10MB
        raise ValueError("MAX_FILE_SIZE must be between 1KB and 10MB")

    # Validate LOG_LEVEL
    valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    if config['LOG_LEVEL'] not in valid_log_levels:
        raise ValueError(f"LOG_LEVEL must be one of: {', '.join(valid_log_levels)}")

    # Validate paths
    if not path.isabs(config['DATA_DIR']):
        raise ValueError("DATA_DIR must be an absolute path")

    return True

def load_config() -> Dict[str, Any]:
    """
    Loads and validates environment variables, initializes configuration settings
    with secure defaults, and ensures data directory exists with proper permissions.

    Returns:
        Dict[str, Any]: Validated configuration dictionary with all settings
    """
    # Load environment variables from .env file
    load_dotenv()

    # Initialize configuration dictionary
    config = {
        'DEBUG': DEBUG,
        'DATA_DIR': DATA_DIR,
        'TASKS_FILE': TASKS_FILE,
        'BACKUP_FILE': BACKUP_FILE,
        'FILE_PERMISSIONS': FILE_PERMISSIONS,
        'MAX_TASKS': MAX_TASKS,
        'MAX_DESCRIPTION_LENGTH': MAX_DESCRIPTION_LENGTH,
        'OPERATION_TIMEOUT': OPERATION_TIMEOUT,
        'MAX_FILE_SIZE': MAX_FILE_SIZE,
        'LOG_LEVEL': LOG_LEVEL
    }

    # Validate configuration
    validate_config(config)

    # Ensure data directory exists with proper permissions
    if not path.exists(config['DATA_DIR']):
        os.makedirs(config['DATA_DIR'], mode=config['FILE_PERMISSIONS'])
    else:
        # Update permissions on existing directory
        os.chmod(config['DATA_DIR'], config['FILE_PERMISSIONS'])

    # Cache configuration
    global CONFIG_CACHE
    CONFIG_CACHE = config

    return config

def get_config() -> Dict[str, Any]:
    """
    Retrieves current configuration settings from cache or loads if not cached.

    Returns:
        Dict[str, Any]: Current configuration dictionary
    """
    global CONFIG_CACHE
    if CONFIG_CACHE is None:
        return load_config()
    return CONFIG_CACHE