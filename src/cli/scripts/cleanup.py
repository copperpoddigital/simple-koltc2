"""
Cleanup script for the Simple To-Do List application.

Handles secure cleanup of old tasks, log files, and backup files with proper
error handling and logging according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional

from ..logging.logger import get_logger
from ..data.storage import TaskStorage
from ..config.settings import DATA_DIR, MAX_FILE_SIZE, FILE_PERMISSIONS

# Initialize logger
logger = get_logger()

# Constants for cleanup operations
CLEANUP_INTERVAL_DAYS = 30  # Tasks older than this will be cleaned up
MAX_BACKUP_FILES = 5  # Maximum number of backup files to retain

def cleanup_old_tasks(storage: TaskStorage) -> int:
    """
    Removes completed tasks older than the cleanup interval.

    Args:
        storage: TaskStorage instance for task operations

    Returns:
        int: Number of tasks cleaned up

    Raises:
        FileAccessError: If file operations fail
    """
    try:
        tasks = storage.get_all_tasks()
        cutoff_date = datetime.utcnow() - timedelta(days=CLEANUP_INTERVAL_DAYS)
        initial_count = len(tasks)

        # Filter tasks to keep
        tasks_to_keep = [
            task for task in tasks
            if task.status != 'completed' or
            datetime.fromisoformat(task.modified) > cutoff_date
        ]

        # Calculate number of removed tasks
        removed_count = initial_count - len(tasks_to_keep)

        if removed_count > 0:
            # Update storage with filtered tasks
            storage._tasks = tasks_to_keep
            storage.save_tasks()
            logger.info(f"Cleaned up {removed_count} old completed tasks")
        else:
            logger.info("No old tasks to clean up")

        return removed_count

    except Exception as e:
        logger.error(f"Task cleanup failed: {str(e)}")
        raise

def cleanup_log_files() -> bool:
    """
    Manages log file rotation and cleanup.

    Returns:
        bool: True if cleanup successful

    Raises:
        FileAccessError: If file operations fail
    """
    try:
        log_dir = os.path.join(DATA_DIR, 'logs')
        if not os.path.exists(log_dir):
            logger.info("No log directory found")
            return True

        cutoff_date = datetime.utcnow() - timedelta(days=CLEANUP_INTERVAL_DAYS)
        cleaned_count = 0

        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)
            if not os.path.isfile(file_path):
                continue

            # Check file size and age
            stats = os.stat(file_path)
            file_time = datetime.fromtimestamp(stats.st_mtime)
            
            if stats.st_size > MAX_FILE_SIZE:
                # Rotate oversized log files
                backup_path = f"{file_path}.1"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(file_path, backup_path)
                os.chmod(backup_path, FILE_PERMISSIONS)
                cleaned_count += 1
            
            elif file_time < cutoff_date:
                # Remove old log files
                os.remove(file_path)
                cleaned_count += 1

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} log files")
        else:
            logger.info("No log files needed cleanup")

        return True

    except Exception as e:
        logger.error(f"Log cleanup failed: {str(e)}")
        return False

def cleanup_backup_files() -> bool:
    """
    Manages backup file retention.

    Returns:
        bool: True if cleanup successful

    Raises:
        FileAccessError: If file operations fail
    """
    try:
        if not os.path.exists(DATA_DIR):
            logger.info("No data directory found")
            return True

        # Get list of backup files
        backup_files = []
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.bak'):
                file_path = os.path.join(DATA_DIR, filename)
                stats = os.stat(file_path)
                backup_files.append((file_path, stats.st_mtime))

        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)

        # Remove excess backup files
        removed_count = 0
        for file_path, _ in backup_files[MAX_BACKUP_FILES:]:
            os.remove(file_path)
            removed_count += 1

        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} excess backup files")
        else:
            logger.info("No backup files needed cleanup")

        # Verify permissions on remaining backups
        for file_path, _ in backup_files[:MAX_BACKUP_FILES]:
            if os.path.exists(file_path):
                os.chmod(file_path, FILE_PERMISSIONS)

        return True

    except Exception as e:
        logger.error(f"Backup cleanup failed: {str(e)}")
        return False

def main() -> int:
    """
    Main cleanup orchestration function.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info("Starting cleanup operations")
        success = True

        # Initialize storage
        storage = TaskStorage()

        # Cleanup old tasks
        try:
            removed_tasks = cleanup_old_tasks(storage)
            logger.info(f"Task cleanup completed: {removed_tasks} tasks removed")
        except Exception as e:
            logger.error(f"Task cleanup failed: {str(e)}")
            success = False

        # Cleanup log files
        if not cleanup_log_files():
            success = False

        # Cleanup backup files
        if not cleanup_backup_files():
            success = False

        if success:
            logger.info("All cleanup operations completed successfully")
            return 0
        else:
            logger.error("Some cleanup operations failed")
            return 1

    except Exception as e:
        logger.error(f"Cleanup script failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())