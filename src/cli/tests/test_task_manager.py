"""
Comprehensive test suite for TaskManager class validating core functionality,
performance, security, and data integrity with enterprise-grade testing standards.

Version: 1.0
Python: 3.6+
"""

import os
import pytest  # version: 6.0.0+
import time
from datetime import datetime
from typing import List, Dict, Any
from memory_profiler import profile  # version: 0.60.0+

from ..core.task_manager import TaskManager
from ..models.task import Task
from ..exceptions.task_exceptions import TaskValidationError, TaskNotFoundError, TaskLimitError
from ..exceptions.storage_exceptions import FileAccessError, DataCorruptionError

# Test fixtures and configuration
@pytest.fixture
def temp_storage_path(tmp_path) -> str:
    """Provides temporary storage path for tests."""
    return str(tmp_path / "test_tasks.json")

@pytest.fixture
def task_manager(temp_storage_path) -> TaskManager:
    """Provides clean TaskManager instance for each test."""
    manager = TaskManager(temp_storage_path)
    yield manager
    # Cleanup
    if os.path.exists(temp_storage_path):
        os.remove(temp_storage_path)

@pytest.fixture
def sample_tasks() -> List[Dict[str, Any]]:
    """Provides sample task data for testing."""
    return [
        {"description": "Test task 1", "status": "pending"},
        {"description": "Test task 2", "status": "completed"},
        {"description": "Test task 3", "status": "pending"}
    ]

# Core functionality tests
class TestTaskCreation:
    """Test suite for task creation functionality."""

    def test_create_task_success(self, task_manager: TaskManager):
        """Validates successful task creation with proper data validation."""
        description = "Test task"
        task = task_manager.create_task(description)
        
        assert task is not None
        assert task.id > 0
        assert task.description == description
        assert task.status == "pending"
        assert isinstance(task.created, datetime)
        assert isinstance(task.modified, datetime)

    @pytest.mark.parametrize("invalid_description", [
        "",  # Empty string
        "a" * 201,  # Too long
        None,  # None value
        "<script>alert('xss')</script>",  # Injection attempt
        "   ",  # Whitespace only
    ])
    def test_create_task_validation(self, task_manager: TaskManager, invalid_description):
        """Tests task creation with invalid inputs."""
        with pytest.raises(TaskValidationError):
            task_manager.create_task(invalid_description)

    def test_create_task_limit(self, task_manager: TaskManager):
        """Validates task limit enforcement."""
        # Create maximum allowed tasks
        for i in range(1000):
            task_manager.create_task(f"Task {i}")

        # Attempt to exceed limit
        with pytest.raises(TaskLimitError):
            task_manager.create_task("Exceeding limit")

class TestTaskRetrieval:
    """Test suite for task retrieval operations."""

    def test_get_task_success(self, task_manager: TaskManager):
        """Validates successful task retrieval."""
        # Create test task
        created_task = task_manager.create_task("Test task")
        
        # Retrieve task
        retrieved_task = task_manager.get_task(created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.description == created_task.description

    def test_get_task_not_found(self, task_manager: TaskManager):
        """Validates proper handling of non-existent task retrieval."""
        with pytest.raises(TaskNotFoundError):
            task_manager.get_task(999)

    def test_get_all_tasks(self, task_manager: TaskManager, sample_tasks):
        """Validates retrieval of all tasks."""
        # Create sample tasks
        created_tasks = []
        for task_data in sample_tasks:
            task = task_manager.create_task(task_data["description"])
            created_tasks.append(task)

        # Retrieve all tasks
        all_tasks = task_manager.get_all_tasks()
        
        assert len(all_tasks) == len(sample_tasks)
        assert all(isinstance(task, Task) for task in all_tasks)

class TestTaskCompletion:
    """Test suite for task completion functionality."""

    def test_complete_task_success(self, task_manager: TaskManager):
        """Validates successful task completion."""
        # Create test task
        task = task_manager.create_task("Test task")
        
        # Complete task
        assert task_manager.complete_task(task.id) is True
        
        # Verify completion
        updated_task = task_manager.get_task(task.id)
        assert updated_task.status == "completed"
        assert updated_task.modified > task.modified

    def test_complete_nonexistent_task(self, task_manager: TaskManager):
        """Validates handling of completing non-existent task."""
        with pytest.raises(TaskNotFoundError):
            task_manager.complete_task(999)

# Performance tests
@pytest.mark.performance
class TestPerformance:
    """Test suite for performance requirements."""

    @profile
    def test_task_operations_performance(self, task_manager: TaskManager):
        """Validates performance metrics for core operations."""
        # Measure task creation time
        start_time = time.time()
        task = task_manager.create_task("Performance test task")
        creation_time = (time.time() - start_time) * 1000
        assert creation_time < 500, "Task creation exceeded 500ms limit"

        # Measure task retrieval time
        start_time = time.time()
        task_manager.get_task(task.id)
        retrieval_time = (time.time() - start_time) * 1000
        assert retrieval_time < 200, "Task retrieval exceeded 200ms limit"

        # Measure task completion time
        start_time = time.time()
        task_manager.complete_task(task.id)
        completion_time = (time.time() - start_time) * 1000
        assert completion_time < 500, "Task completion exceeded 500ms limit"

    def test_bulk_operation_performance(self, task_manager: TaskManager):
        """Tests performance with larger data sets."""
        # Create 100 tasks and measure time
        start_time = time.time()
        tasks = []
        for i in range(100):
            task = task_manager.create_task(f"Bulk test task {i}")
            tasks.append(task)
        bulk_creation_time = (time.time() - start_time) * 1000
        
        assert bulk_creation_time < 5000, "Bulk creation exceeded 5000ms limit"

# Security and data integrity tests
@pytest.mark.security
class TestSecurity:
    """Test suite for security and data integrity."""

    def test_data_integrity(self, task_manager: TaskManager, temp_storage_path):
        """Validates data integrity and corruption handling."""
        # Create test task
        original_task = task_manager.create_task("Integrity test task")

        # Corrupt storage file
        with open(temp_storage_path, 'a') as f:
            f.write("corrupted data")

        # Verify corruption handling
        with pytest.raises(DataCorruptionError):
            TaskManager(temp_storage_path)

    def test_input_sanitization(self, task_manager: TaskManager):
        """Tests input sanitization and injection prevention."""
        dangerous_inputs = [
            "'; DROP TABLE tasks; --",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "\x00\x1f\x7f",
            "{{7*7}}"
        ]
        
        for dangerous_input in dangerous_inputs:
            with pytest.raises(TaskValidationError):
                task_manager.create_task(dangerous_input)

    def test_concurrent_access(self, task_manager: TaskManager):
        """Tests handling of concurrent access attempts."""
        task = task_manager.create_task("Concurrent test task")
        
        # Simulate concurrent completion attempts
        task_manager.complete_task(task.id)
        with pytest.raises(TaskValidationError):
            task_manager.complete_task(task.id)  # Already completed

if __name__ == '__main__':
    pytest.main(['-v', __file__])