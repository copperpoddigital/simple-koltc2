"""
Pytest configuration and fixtures for the Simple To-Do List application test suite.

This module provides secure test fixtures, performance monitoring, and comprehensive
test data validation according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import os
import tempfile
import pytest
from datetime import datetime
from typing import List, Dict, Any, Generator

from ..models.task import Task
from ..data.storage import TaskStorage
from ..core.task_manager import TaskManager

# Test data constants with secure defaults
TEST_FILE_PERMISSIONS = 0o600
MAX_TEST_TASKS = 10
PERFORMANCE_THRESHOLD_MS = 1000  # 1 second max per operation

@pytest.fixture(scope="function")
def temp_storage_path() -> Generator[str, None, None]:
    """
    Provides a secure temporary file path for test storage with guaranteed cleanup.
    
    Yields:
        str: Path to temporary storage file with proper permissions
    """
    try:
        # Create temporary directory with secure permissions
        temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, TEST_FILE_PERMISSIONS)
        
        # Create temporary file path
        temp_file = os.path.join(temp_dir, "test_tasks.json")
        
        yield temp_file
        
    finally:
        # Ensure cleanup of test files
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@pytest.fixture(scope="function")
def task_storage(temp_storage_path: str) -> TaskStorage:
    """
    Provides a TaskStorage instance with performance monitoring.
    
    Args:
        temp_storage_path: Path to temporary storage file
        
    Returns:
        TaskStorage: Configured storage instance
    """
    storage = TaskStorage(temp_storage_path)
    
    # Track performance metrics
    start_time = datetime.utcnow()
    
    yield storage
    
    # Verify performance
    end_time = datetime.utcnow()
    duration_ms = (end_time - start_time).total_seconds() * 1000
    assert duration_ms <= PERFORMANCE_THRESHOLD_MS, f"Storage operation exceeded {PERFORMANCE_THRESHOLD_MS}ms threshold"
    
    # Cleanup
    if os.path.exists(temp_storage_path):
        os.unlink(temp_storage_path)

@pytest.fixture(scope="function")
def task_manager(task_storage: TaskStorage) -> TaskManager:
    """
    Provides a TaskManager instance with transaction support.
    
    Args:
        task_storage: TaskStorage fixture
        
    Returns:
        TaskManager: Configured manager instance
    """
    manager = TaskManager(task_storage._file_path)
    
    # Initialize performance tracking
    manager._performance_metrics = {}
    
    yield manager
    
    # Verify performance metrics
    for operation, duration in manager.get_performance_metrics().items():
        assert duration <= PERFORMANCE_THRESHOLD_MS, \
            f"Operation {operation} exceeded {PERFORMANCE_THRESHOLD_MS}ms threshold"

@pytest.fixture(scope="function")
def sample_tasks() -> List[Task]:
    """
    Provides a comprehensive set of test tasks with boundary conditions.
    
    Returns:
        List[Task]: List of validated Task instances
    """
    tasks = [
        Task(
            id=1,
            description="Normal task",
            status="pending",
            created=datetime.utcnow(),
            modified=datetime.utcnow()
        ),
        Task(
            id=2,
            description="A" * 200,  # Maximum length
            status="pending",
            created=datetime.utcnow(),
            modified=datetime.utcnow()
        ),
        Task(
            id=3,
            description="Task with punctuation: Hello, World!",
            status="completed",
            created=datetime.utcnow(),
            modified=datetime.utcnow()
        )
    ]
    
    # Validate all test tasks
    for task in tasks:
        task.validate()
    
    return tasks

@pytest.fixture(scope="session")
def performance_metrics() -> Dict[str, float]:
    """
    Provides a container for tracking test performance metrics.
    
    Returns:
        Dict[str, float]: Performance metrics dictionary
    """
    return {
        'storage_operations': 0.0,
        'task_operations': 0.0,
        'validation_time': 0.0
    }

@pytest.fixture(scope="function")
def cleanup_test_files() -> None:
    """
    Ensures proper cleanup of any test files after each test.
    """
    yield
    
    # Clean up any remaining test files
    test_patterns = ['test_*.json', '*.bak']
    for pattern in test_patterns:
        for file in tempfile.gettempdir().glob(pattern):
            try:
                os.unlink(file)
            except (OSError, PermissionError):
                continue

@pytest.fixture(autouse=True)
def verify_file_permissions() -> None:
    """
    Automatically verifies secure file permissions after each test.
    """
    yield
    
    # Check permissions of any remaining test files
    test_dir = tempfile.gettempdir()
    for file in os.listdir(test_dir):
        if file.startswith('test_'):
            file_path = os.path.join(test_dir, file)
            if os.path.exists(file_path):
                mode = os.stat(file_path).st_mode & 0o777
                assert mode <= TEST_FILE_PERMISSIONS, \
                    f"Insecure file permissions detected: {oct(mode)}"