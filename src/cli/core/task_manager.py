"""
Core task management component for the Simple To-Do List application.

This module implements secure task operations with comprehensive validation,
performance monitoring, and atomic transactions according to technical specifications.

Version: 1.0
Python: 3.6+
"""

from datetime import datetime
import time
import logging
from typing import Dict, List, Optional, Tuple

from ..models.task import Task
from ..data.storage import TaskStorage
from .validators import validate_task_description, validate_task_number, sanitize_input
from ..exceptions.task_exceptions import TaskNotFoundError, TaskLimitError
from ..exceptions.validation_exceptions import ValidationError
from ..constants.messages import SUCCESS_MESSAGES, ERROR_MESSAGES

# Initialize logger
logger = logging.getLogger(__name__)

class TaskManager:
    """
    Enhanced task manager with security, performance monitoring, and validation features.
    Implements core task operations with proper error handling and atomic transactions.
    """

    def __init__(self, storage_path: str) -> None:
        """
        Initialize task manager with secure storage and monitoring.

        Args:
            storage_path: Path to task storage file

        Raises:
            FileAccessError: If storage initialization fails
        """
        self._storage = TaskStorage(storage_path)
        self._task_cache: Dict[int, Task] = {}
        self._performance_metrics: Dict[str, float] = {}
        self._transaction_active = False
        
        # Load existing tasks into cache
        self._load_cache()
        logger.info("TaskManager initialized successfully")

    def _load_cache(self) -> None:
        """
        Load existing tasks into memory cache with validation.
        """
        try:
            tasks = self._storage.get_all_tasks()
            self._task_cache = {task.id: task for task in tasks}
            logger.debug(f"Loaded {len(tasks)} tasks into cache")
        except Exception as e:
            logger.error(f"Cache loading failed: {str(e)}")
            self._task_cache = {}

    def _measure_performance(func):
        """
        Decorator for monitoring operation performance.
        """
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(self, *args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                self._performance_metrics[func.__name__] = execution_time
                logger.debug(f"{func.__name__} completed in {execution_time:.2f}ms")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {str(e)}")
                raise
        return wrapper

    @_measure_performance
    def create_task(self, description: str) -> Task:
        """
        Create new task with validation and atomic transaction.

        Args:
            description: Task description

        Returns:
            Task: Newly created task

        Raises:
            TaskLimitError: If task limit exceeded
            ValidationError: If description invalid
            FileAccessError: If storage operation fails
        """
        try:
            # Validate task limit
            if len(self._task_cache) >= 1000:
                raise TaskLimitError(1000)

            # Sanitize and validate description
            clean_description = sanitize_input(description)
            validate_task_description(clean_description)

            # Generate new task ID
            new_id = max(self._task_cache.keys(), default=0) + 1

            # Create task with current timestamp
            task = Task(
                id=new_id,
                description=clean_description,
                status='pending',
                created=datetime.utcnow(),
                modified=datetime.utcnow()
            )

            # Atomic transaction
            self._storage.begin_transaction()
            self._storage.add_task(task)
            self._task_cache[task.id] = task
            self._storage.commit_transaction()

            logger.info(f"Task created successfully: ID {task.id}")
            return task

        except Exception as e:
            if self._transaction_active:
                self._storage.rollback_transaction()
            logger.error(f"Task creation failed: {str(e)}")
            raise

    @_measure_performance
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID with cache optimization.

        Args:
            task_id: Task identifier

        Returns:
            Optional[Task]: Task if found, None otherwise

        Raises:
            TaskNotFoundError: If task not found
        """
        try:
            # Validate task number
            validate_task_number(str(task_id), len(self._task_cache))

            # Check cache first
            if task_id in self._task_cache:
                logger.debug(f"Task {task_id} retrieved from cache")
                return self._task_cache[task_id]

            # Fallback to storage
            task = self._storage.get_task(task_id)
            if task:
                self._task_cache[task_id] = task
                return task

            raise TaskNotFoundError(task_id)

        except Exception as e:
            logger.error(f"Task retrieval failed: {str(e)}")
            raise

    @_measure_performance
    def get_all_tasks(self, page_size: Optional[int] = None, page_number: Optional[int] = None) -> List[Task]:
        """
        Retrieve all tasks with optional pagination.

        Args:
            page_size: Number of tasks per page
            page_number: Page number to retrieve

        Returns:
            List[Task]: List of tasks

        Raises:
            ValueError: If pagination parameters invalid
        """
        try:
            tasks = list(self._task_cache.values())
            
            # Apply pagination if specified
            if page_size and page_number:
                if page_size < 1 or page_number < 1:
                    raise ValueError("Invalid pagination parameters")
                    
                start_idx = (page_number - 1) * page_size
                end_idx = start_idx + page_size
                tasks = tasks[start_idx:end_idx]

            logger.debug(f"Retrieved {len(tasks)} tasks")
            return tasks

        except Exception as e:
            logger.error(f"Task retrieval failed: {str(e)}")
            raise

    @_measure_performance
    def complete_task(self, task_id: int) -> bool:
        """
        Mark task as completed with atomic transaction.

        Args:
            task_id: Task identifier

        Returns:
            bool: True if task marked complete

        Raises:
            TaskNotFoundError: If task not found
            FileAccessError: If storage operation fails
        """
        try:
            # Validate and retrieve task
            task = self.get_task(task_id)
            if not task:
                raise TaskNotFoundError(task_id)

            # Atomic transaction
            self._storage.begin_transaction()
            
            # Update task status
            task.mark_complete()
            self._storage.update_task(task)
            self._task_cache[task_id] = task
            
            self._storage.commit_transaction()
            
            logger.info(f"Task {task_id} marked complete")
            return True

        except Exception as e:
            if self._transaction_active:
                self._storage.rollback_transaction()
            logger.error(f"Task completion failed: {str(e)}")
            raise

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Retrieve performance metrics for monitoring.

        Returns:
            Dict[str, float]: Operation timing metrics
        """
        return self._performance_metrics.copy()