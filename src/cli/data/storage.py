"""
Storage module for the Simple To-Do List application.

Implements secure file-based task persistence with atomic operations,
proper error handling, and backup mechanisms according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import os
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..models.task import Task
from ..exceptions.storage_exceptions import FileAccessError, DataCorruptionError
from ..utils.file_utils import read_json_file, write_json_file, create_backup
from ..logging.logger import get_logger

# Constants for storage configuration
DEFAULT_FILENAME = "todo_tasks.json"
DATA_VERSION = "1.0"
MAX_TASKS = 1000
MAX_FILE_SIZE = 1048576  # 1MB

# Initialize logger
logger = get_logger()

class TaskStorage:
    """
    Manages task data persistence with secure file operations and atomic writes.
    
    Implements file-based storage with proper error handling, backup mechanisms,
    and data validation according to technical specifications.
    """
    
    def __init__(self, file_path: str = DEFAULT_FILENAME) -> None:
        """
        Initialize storage with file path and load existing data.
        
        Args:
            file_path: Path to task storage file
            
        Raises:
            FileAccessError: If file access or permissions fail
        """
        self._file_path = os.path.abspath(os.path.expanduser(file_path))
        self._tasks: List[Task] = []
        self._metadata: Dict[str, Any] = {
            "version": DATA_VERSION,
            "last_modified": datetime.utcnow().isoformat(),
            "task_count": 0
        }
        
        # Ensure storage directory exists with proper permissions
        os.makedirs(os.path.dirname(self._file_path), mode=0o600, exist_ok=True)
        
        # Load existing data if file exists
        if os.path.exists(self._file_path):
            self.load_tasks()
        else:
            # Initialize new storage
            self.save_tasks()
    
    def load_tasks(self) -> List[Task]:
        """
        Load tasks from storage file with validation and error handling.
        
        Returns:
            List[Task]: List of loaded tasks
            
        Raises:
            FileAccessError: If file access fails
            DataCorruptionError: If data is invalid
        """
        try:
            data = read_json_file(self._file_path)
            
            # Validate data structure
            if not isinstance(data, dict) or "tasks" not in data or "metadata" not in data:
                raise DataCorruptionError("Invalid data structure in storage file")
                
            # Validate version compatibility
            if data["metadata"].get("version") != DATA_VERSION:
                raise DataCorruptionError(f"Incompatible data version: {data['metadata'].get('version')}")
                
            # Convert task dictionaries to Task objects
            self._tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]
            self._metadata = data["metadata"]
            
            logger.debug(f"Successfully loaded {len(self._tasks)} tasks from storage")
            return self._tasks
            
        except (FileAccessError, DataCorruptionError) as e:
            logger.error(f"Failed to load tasks: {str(e)}")
            raise
    
    def save_tasks(self) -> bool:
        """
        Save tasks to storage file with atomic writes and backups.
        
        Returns:
            bool: True if save successful
            
        Raises:
            FileAccessError: If file write fails
        """
        try:
            # Update metadata
            self._metadata.update({
                "last_modified": datetime.utcnow().isoformat(),
                "task_count": len(self._tasks)
            })
            
            # Prepare data structure
            data = {
                "tasks": [task.to_dict() for task in self._tasks],
                "metadata": self._metadata
            }
            
            # Perform atomic write with backup
            write_json_file(self._file_path, data)
            logger.debug("Successfully saved tasks to storage")
            return True
            
        except FileAccessError as e:
            logger.error(f"Failed to save tasks: {str(e)}")
            raise
    
    def add_task(self, task: Task) -> bool:
        """
        Add new task with validation and persistence.
        
        Args:
            task: Task object to add
            
        Returns:
            bool: True if task added successfully
            
        Raises:
            ValueError: If task limit exceeded
            FileAccessError: If save fails
        """
        if len(self._tasks) >= MAX_TASKS:
            raise ValueError(f"Task limit of {MAX_TASKS} exceeded")
            
        self._tasks.append(task)
        return self.save_tasks()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID with error handling.
        
        Args:
            task_id: ID of task to retrieve
            
        Returns:
            Optional[Task]: Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task: Task) -> bool:
        """
        Update existing task with validation and persistence.
        
        Args:
            task: Updated task object
            
        Returns:
            bool: True if update successful
            
        Raises:
            ValueError: If task not found
            FileAccessError: If save fails
        """
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                self._tasks[i] = task
                return self.save_tasks()
        raise ValueError(f"Task with ID {task.id} not found")
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks with optional filtering.
        
        Returns:
            List[Task]: List of all tasks
        """
        return self._tasks.copy()