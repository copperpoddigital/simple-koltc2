"""
Utility module for secure file operations in the Simple To-Do List application.

Implements secure file access, atomic writes, JSON operations, backups, and path validation
with comprehensive error handling and security measures.

Version: 1.0
Python: 3.6+
"""

import os
import json
import shutil
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path

from ..config.settings import FILE_SETTINGS
from ..exceptions.storage_exceptions import FileAccessError, DataCorruptionError
from ..logging.logger import get_logger

# Initialize logger for file operations
logger = get_logger()

def validate_file_path(file_path: str) -> bool:
    """
    Validates file path for security and accessibility.

    Args:
        file_path: Path to validate

    Returns:
        bool: True if path is valid and secure

    Raises:
        FileAccessError: If path validation fails
    """
    try:
        # Expand user path and convert to absolute
        full_path = os.path.abspath(os.path.expanduser(file_path))
        path_obj = Path(full_path)

        # Security checks
        if not path_obj.parent.exists():
            os.makedirs(path_obj.parent, mode=FILE_SETTINGS['FILE_PERMISSIONS'])

        # Verify path is within user's home directory
        if not str(path_obj).startswith(os.path.expanduser('~')):
            raise FileAccessError("Access denied: Path must be within user's home directory")

        # Check for dangerous patterns
        dangerous_patterns = ['..', '//', '\\\\']
        if any(pattern in str(path_obj) for pattern in dangerous_patterns):
            raise FileAccessError("Invalid path: Contains dangerous patterns")

        # Verify permissions if file exists
        if path_obj.exists():
            current_mode = os.stat(path_obj).st_mode & 0o777
            if current_mode != FILE_SETTINGS['FILE_PERMISSIONS']:
                os.chmod(path_obj, FILE_SETTINGS['FILE_PERMISSIONS'])

        logger.debug(f"Path validation successful: {file_path}")
        return True

    except (OSError, PermissionError) as e:
        logger.error(f"Path validation failed: {str(e)}")
        raise FileAccessError(f"Unable to access path: {file_path}")

def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Reads and parses JSON data from file with security checks.

    Args:
        file_path: Path to JSON file

    Returns:
        dict: Parsed JSON data

    Raises:
        FileAccessError: If file access fails
        DataCorruptionError: If JSON parsing fails
    """
    try:
        validate_file_path(file_path)
        
        if not os.path.exists(file_path):
            logger.info(f"File not found, returning empty data: {file_path}")
            return {"tasks": [], "metadata": {"version": "1.0", "task_count": 0}}

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate basic structure
        if not isinstance(data, dict) or "tasks" not in data or "metadata" not in data:
            raise DataCorruptionError("Invalid data structure in JSON file")

        logger.debug(f"Successfully read JSON file: {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {str(e)}")
        raise DataCorruptionError("Invalid JSON format in file")
    except (OSError, PermissionError) as e:
        logger.error(f"File read failed: {str(e)}")
        raise FileAccessError(f"Unable to read file: {file_path}")

def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Writes data to JSON file atomically with backup creation.

    Args:
        file_path: Target file path
        data: Data to write

    Returns:
        bool: True if write successful

    Raises:
        FileAccessError: If file write fails
    """
    try:
        validate_file_path(file_path)
        
        # Create backup if file exists
        if os.path.exists(file_path):
            create_backup(file_path)

        # Create temporary file for atomic write
        temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(file_path))
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Set proper permissions before moving
            os.chmod(temp_path, FILE_SETTINGS['FILE_PERMISSIONS'])
            
            # Atomic replace
            os.replace(temp_path, file_path)
            
            logger.debug(f"Successfully wrote JSON file: {file_path}")
            return True

        finally:
            # Clean up temp file if still exists
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except (OSError, PermissionError) as e:
        logger.error(f"File write failed: {str(e)}")
        raise FileAccessError(f"Unable to write file: {file_path}")

def create_backup(file_path: str) -> str:
    """
    Creates secure backup of specified file.

    Args:
        file_path: Path to file to backup

    Returns:
        str: Path to backup file

    Raises:
        FileAccessError: If backup creation fails
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"No file to backup: {file_path}")
            return ""

        backup_path = f"{file_path}.bak"
        validate_file_path(backup_path)

        # Secure copy with metadata preservation
        shutil.copy2(file_path, backup_path)
        os.chmod(backup_path, FILE_SETTINGS['FILE_PERMISSIONS'])

        logger.debug(f"Successfully created backup: {backup_path}")
        return backup_path

    except (OSError, PermissionError) as e:
        logger.error(f"Backup creation failed: {str(e)}")
        raise FileAccessError(f"Unable to create backup: {file_path}")