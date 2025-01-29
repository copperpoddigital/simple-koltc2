"""
Comprehensive test suite for the TaskStorage class.

Tests data persistence, file operations, task management, error handling,
security measures, and performance benchmarks according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import os
import json
import stat
import tempfile
from datetime import datetime
from typing import List, Dict, Any
import pytest  # version: 6.0.0+

from ..data.storage import TaskStorage
from ..models.task import Task
from ..exceptions.storage_exceptions import FileAccessError, DataCorruptionError
from ..config.settings import FILE_SETTINGS

# Test constants
TEST_TASK_COUNT = 100
MAX_TASKS = 1000
PERFORMANCE_THRESHOLDS = {
    'task_addition': 100,  # ms
    'task_retrieval': 200,  # ms
    'file_save': 300,      # ms
}

@pytest.fixture
def temp_storage_path() -> str:
    """
    Creates a temporary storage file with proper permissions.
    
    Returns:
        str: Path to temporary storage file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tf:
        temp_path = tf.name
    os.chmod(temp_path, FILE_SETTINGS['FILE_PERMISSIONS'])
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def task_storage(temp_storage_path: str) -> TaskStorage:
    """
    Provides a clean TaskStorage instance for each test.
    
    Args:
        temp_storage_path: Path to temporary storage file
        
    Returns:
        TaskStorage: Initialized storage instance
    """
    storage = TaskStorage(temp_storage_path)
    yield storage
    if os.path.exists(temp_storage_path):
        os.unlink(temp_storage_path)

@pytest.fixture
def sample_tasks() -> List[Task]:
    """
    Generates a list of sample tasks for testing.
    
    Returns:
        List[Task]: List of sample Task objects
    """
    return [
        Task(
            id=i,
            description=f"Test task {i}",
            status='pending',
            created=datetime.utcnow(),
            modified=datetime.utcnow()
        )
        for i in range(TEST_TASK_COUNT)
    ]

def test_storage_initialization(temp_storage_path: str):
    """Tests TaskStorage initialization with various scenarios."""
    # Test successful initialization
    storage = TaskStorage(temp_storage_path)
    assert os.path.exists(temp_storage_path)
    assert stat.S_IMODE(os.stat(temp_storage_path).st_mode) == FILE_SETTINGS['FILE_PERMISSIONS']
    
    # Test initialization with invalid path
    with pytest.raises(FileAccessError):
        TaskStorage('/invalid/path/tasks.json')
    
    # Test initialization with insufficient permissions
    os.chmod(temp_storage_path, 0o000)
    with pytest.raises(FileAccessError):
        TaskStorage(temp_storage_path)

@pytest.mark.security
def test_file_security(task_storage: TaskStorage):
    """Tests storage security measures and file permissions."""
    file_path = task_storage._file_path
    
    # Verify file permissions
    assert stat.S_IMODE(os.stat(file_path).st_mode) == FILE_SETTINGS['FILE_PERMISSIONS']
    
    # Test backup file permissions
    task_storage.create_backup()
    backup_path = f"{file_path}.bak"
    assert os.path.exists(backup_path)
    assert stat.S_IMODE(os.stat(backup_path).st_mode) == FILE_SETTINGS['FILE_PERMISSIONS']
    
    # Test atomic write operations
    task = Task(1, "Test task", created=datetime.utcnow())
    task_storage.add_task(task)
    assert os.path.exists(file_path)
    assert stat.S_IMODE(os.stat(file_path).st_mode) == FILE_SETTINGS['FILE_PERMISSIONS']

@pytest.mark.persistence
def test_task_persistence(task_storage: TaskStorage, sample_tasks: List[Task]):
    """Tests task data persistence and integrity."""
    # Test task addition and persistence
    for task in sample_tasks[:10]:
        assert task_storage.add_task(task)
    
    # Verify data integrity after reload
    reloaded_storage = TaskStorage(task_storage._file_path)
    stored_tasks = reloaded_storage.get_all_tasks()
    assert len(stored_tasks) == 10
    
    # Verify task data accuracy
    for original, stored in zip(sample_tasks[:10], stored_tasks):
        assert stored.id == original.id
        assert stored.description == original.description
        assert stored.status == original.status
        
    # Test backup creation and restoration
    backup_path = task_storage.create_backup()
    assert os.path.exists(backup_path)
    
    # Corrupt main file and test recovery
    with open(task_storage._file_path, 'w') as f:
        f.write('corrupted data')
    
    with pytest.raises(DataCorruptionError):
        task_storage.load_tasks()
    
    task_storage.restore_from_backup()
    restored_tasks = task_storage.get_all_tasks()
    assert len(restored_tasks) == 10

@pytest.mark.operations
def test_task_operations(task_storage: TaskStorage):
    """Tests task management operations."""
    # Test single task addition
    task = Task(1, "Test task", created=datetime.utcnow())
    assert task_storage.add_task(task)
    
    # Test task retrieval
    stored_task = task_storage.get_task(1)
    assert stored_task is not None
    assert stored_task.id == task.id
    assert stored_task.description == task.description
    
    # Test task update
    stored_task.status = 'completed'
    assert task_storage.update_task(stored_task)
    updated_task = task_storage.get_task(1)
    assert updated_task.status == 'completed'
    
    # Test task limit enforcement
    with pytest.raises(ValueError):
        for i in range(MAX_TASKS + 1):
            task_storage.add_task(Task(i + 2, f"Task {i}", created=datetime.utcnow()))

@pytest.mark.error_handling
def test_error_handling(task_storage: TaskStorage):
    """Tests error handling and recovery mechanisms."""
    # Test file access error
    os.chmod(task_storage._file_path, 0o000)
    with pytest.raises(FileAccessError):
        task_storage.save_tasks()
    
    # Test data corruption handling
    os.chmod(task_storage._file_path, FILE_SETTINGS['FILE_PERMISSIONS'])
    with open(task_storage._file_path, 'w') as f:
        f.write('{"invalid": "json"')
    
    with pytest.raises(DataCorruptionError):
        task_storage.load_tasks()
    
    # Test invalid task data
    with pytest.raises(ValueError):
        task_storage.update_task(Task(999, "Nonexistent task"))

@pytest.mark.benchmark
def test_performance(task_storage: TaskStorage, sample_tasks: List[Task], benchmark):
    """Tests storage operation performance against benchmarks."""
    # Test task addition performance
    def add_task():
        task_storage.add_task(sample_tasks[0])
    
    result = benchmark(add_task)
    assert result.stats['mean'] * 1000 < PERFORMANCE_THRESHOLDS['task_addition']
    
    # Test task retrieval performance
    task_storage.add_task(sample_tasks[0])
    
    def get_task():
        task_storage.get_task(sample_tasks[0].id)
    
    result = benchmark(get_task)
    assert result.stats['mean'] * 1000 < PERFORMANCE_THRESHOLDS['task_retrieval']
    
    # Test file save performance
    def save_tasks():
        task_storage.save_tasks()
    
    result = benchmark(save_tasks)
    assert result.stats['mean'] * 1000 < PERFORMANCE_THRESHOLDS['file_save']

@pytest.mark.stress
def test_stress_conditions(task_storage: TaskStorage, sample_tasks: List[Task]):
    """Tests storage behavior under stress conditions."""
    # Test large dataset handling
    for task in sample_tasks:
        task_storage.add_task(task)
    assert len(task_storage.get_all_tasks()) == TEST_TASK_COUNT
    
    # Test rapid consecutive operations
    for _ in range(100):
        task_storage.save_tasks()
        task_storage.load_tasks()
    
    # Verify data integrity after stress
    stored_tasks = task_storage.get_all_tasks()
    assert len(stored_tasks) == TEST_TASK_COUNT
    for original, stored in zip(sample_tasks, stored_tasks):
        assert stored.id == original.id
        assert stored.description == original.description