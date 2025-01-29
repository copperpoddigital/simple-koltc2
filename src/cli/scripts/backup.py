"""
Backup script for the Simple To-Do List application.

Implements secure backup functionality with proper permissions, validation,
and error handling according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import os  # version: 3.6+
import datetime  # version: 3.6+
import argparse  # version: 3.6+

from ..data.storage import TaskStorage
from ..utils.file_utils import create_backup
from ..logging.logger import get_logger
from ..exceptions.storage_exceptions import FileAccessError

# Initialize logger
logger = get_logger()

# Constants
BACKUP_SUFFIX = ".bak"

def create_timestamped_backup(file_path: str) -> str:
    """
    Creates a timestamped backup of the task data file with secure permissions.

    Args:
        file_path: Path to the task data file to backup

    Returns:
        str: Path to created backup file

    Raises:
        FileAccessError: If backup creation fails
    """
    try:
        # Validate source file exists
        if not os.path.exists(file_path):
            raise FileAccessError(f"Source file not found: {file_path}")

        # Generate timestamp for backup file name
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}_{timestamp}{BACKUP_SUFFIX}"

        # Create backup with secure permissions
        created_backup = create_backup(file_path)
        if not created_backup:
            raise FileAccessError("Backup creation failed")

        # Rename backup with timestamp
        os.rename(created_backup, backup_path)

        # Verify backup file exists and has correct permissions
        if not os.path.exists(backup_path):
            raise FileAccessError("Backup file verification failed")

        logger.info(f"Successfully created backup: {backup_path}")
        return backup_path

    except (OSError, PermissionError) as e:
        logger.error(f"Backup creation failed: {str(e)}")
        raise FileAccessError(f"Unable to create backup: {str(e)}")

def main() -> int:
    """
    Main entry point for backup script with argument parsing and error handling.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(description="Create backup of task data file")
    parser.add_argument(
        "--file",
        help="Path to task data file",
        required=True
    )
    
    try:
        args = parser.parse_args()
        
        # Initialize storage and validate file
        storage = TaskStorage(args.file)
        
        # Create timestamped backup
        backup_path = create_timestamped_backup(args.file)
        logger.info(f"Backup created successfully at: {backup_path}")
        return 0
        
    except FileAccessError as e:
        logger.error(f"Backup failed: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during backup: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())