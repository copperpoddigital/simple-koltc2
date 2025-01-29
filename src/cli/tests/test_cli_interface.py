"""
Comprehensive test suite for the CLI interface component of the Simple To-Do List application.
Implements enterprise-grade testing for user interactions, task management, performance validation,
and security measures according to technical specifications.

Version: 1.0
Python: 3.6+
"""

import pytest  # version: 6.0.0+
from unittest.mock import Mock, patch  # version: 3.6+
import time  # version: 3.6+
from typing import Tuple, List, Dict, Any  # version: 3.6+
import os
import tempfile

from ..interfaces.cli_interface import CLIInterface
from ..interfaces.menu_interface import MenuInterface
from ..core.task_manager import TaskManager, TaskError
from ..models.task import Task
from ..exceptions.task_exceptions import TaskValidationError, TaskNotFoundError
from ..constants.messages import SUCCESS_MESSAGES, ERROR_MESSAGES

@pytest.fixture
def setup_test_environment() -> Tuple[CLIInterface, Mock, str]:
    """
    Sets up test environment with temporary storage and mocked interfaces.
    
    Returns:
        Tuple containing CLI interface instance, mocked menu interface, and temp path
    """
    # Create temporary directory for test storage
    temp_dir = tempfile.mkdtemp()
    storage_path = os.path.join(temp_dir, 'test_tasks.json')
    
    # Create mock menu interface
    mock_menu = Mock(spec=MenuInterface)
    
    # Initialize CLI interface with mocked components
    cli = CLIInterface(storage_path)
    cli._menu_interface = mock_menu
    
    yield cli, mock_menu, storage_path
    
    # Cleanup
    if os.path.exists(storage_path):
        os.remove(storage_path)
    os.rmdir(temp_dir)

@pytest.mark.unit
def test_cli_initialization(setup_test_environment):
    """
    Tests CLI interface initialization and component setup.
    Verifies proper initialization of task manager and menu interface.
    """
    cli, mock_menu, storage_path = setup_test_environment
    
    # Verify component initialization
    assert isinstance(cli._task_manager, TaskManager)
    assert cli._menu_interface == mock_menu
    assert not cli._running
    
    # Verify performance metrics initialization
    assert 'menu_response' in cli._performance_metrics
    assert 'task_operations' in cli._performance_metrics
    assert 'total_runtime' in cli._performance_metrics
    
    # Verify session state initialization
    assert cli._session_state['tasks_added'] == 0
    assert cli._session_state['tasks_completed'] == 0
    assert cli._session_state['operations_performed'] == 0
    assert cli._session_state['last_operation'] is None

@pytest.mark.integration
@pytest.mark.timed
def test_add_task_flow(setup_test_environment):
    """
    Tests complete task addition workflow with performance validation.
    Verifies task creation, storage, and response time requirements.
    """
    cli, mock_menu, _ = setup_test_environment
    test_description = "Test task description"
    
    # Mock menu interface responses
    mock_menu.display_task_input.return_value = test_description
    
    # Start performance timer
    start_time = time.time()
    
    # Execute add task operation
    cli.handle_add_task()
    
    # Verify performance
    operation_time = (time.time() - start_time) * 1000
    assert operation_time < 500, "Task addition exceeded 500ms limit"
    
    # Verify task creation
    tasks = cli._task_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == test_description
    assert tasks[0].status == "pending"
    
    # Verify session state update
    assert cli._session_state['tasks_added'] == 1
    
    # Verify success message
    mock_menu.show_message.assert_called_with(SUCCESS_MESSAGES['task_added'], 'success')

@pytest.mark.integration
@pytest.mark.timed
def test_view_tasks_flow(setup_test_environment):
    """
    Tests task viewing functionality with performance validation.
    Verifies task list display and response time requirements.
    """
    cli, mock_menu, _ = setup_test_environment
    
    # Add test tasks
    test_tasks = [
        Task(id=1, description="Task 1", status="pending"),
        Task(id=2, description="Task 2", status="completed")
    ]
    for task in test_tasks:
        cli._task_manager._task_cache[task.id] = task
    
    # Start performance timer
    start_time = time.time()
    
    # Execute view tasks operation
    cli.handle_view_tasks()
    
    # Verify performance
    operation_time = (time.time() - start_time) * 1000
    assert operation_time < 200, "Task viewing exceeded 200ms limit"
    
    # Verify task list display
    mock_menu.display_task_list.assert_called_once()
    displayed_tasks = mock_menu.display_task_list.call_args[0][0]
    assert len(displayed_tasks) == 2
    assert all(isinstance(task, Task) for task in displayed_tasks)

@pytest.mark.integration
@pytest.mark.timed
def test_complete_task_flow(setup_test_environment):
    """
    Tests task completion workflow with validation.
    Verifies status updates, storage, and response time requirements.
    """
    cli, mock_menu, _ = setup_test_environment
    
    # Add test task
    test_task = Task(id=1, description="Test task", status="pending")
    cli._task_manager._task_cache[test_task.id] = test_task
    
    # Mock menu interface responses
    mock_menu.display_completion_menu.return_value = 1
    
    # Start performance timer
    start_time = time.time()
    
    # Execute complete task operation
    cli.handle_complete_task()
    
    # Verify performance
    operation_time = (time.time() - start_time) * 1000
    assert operation_time < 500, "Task completion exceeded 500ms limit"
    
    # Verify task status update
    updated_task = cli._task_manager.get_task(1)
    assert updated_task.status == "completed"
    
    # Verify session state update
    assert cli._session_state['tasks_completed'] == 1
    
    # Verify success message
    mock_menu.show_message.assert_called_with(SUCCESS_MESSAGES['task_completed'], 'success')

@pytest.mark.security
def test_input_validation(setup_test_environment):
    """
    Tests input validation and security measures.
    Verifies proper handling of invalid inputs and security constraints.
    """
    cli, mock_menu, _ = setup_test_environment
    
    # Test invalid task description
    mock_menu.display_task_input.return_value = "a" * 201  # Exceeds max length
    with pytest.raises(TaskValidationError):
        cli.handle_add_task()
    
    # Test special character injection
    mock_menu.display_task_input.return_value = "Task with <script>alert('xss')</script>"
    with pytest.raises(TaskValidationError):
        cli.handle_add_task()
    
    # Test invalid task number
    mock_menu.display_completion_menu.return_value = 999  # Non-existent task
    with pytest.raises(TaskNotFoundError):
        cli.handle_complete_task()
    
    # Verify error messages
    mock_menu.show_message.assert_called_with(
        pytest.raises(TaskValidationError).match("Task validation failed"),
        'error'
    )

@pytest.mark.integration
def test_error_handling(setup_test_environment):
    """
    Tests comprehensive error handling scenarios.
    Verifies proper handling of various error conditions and system recovery.
    """
    cli, mock_menu, storage_path = setup_test_environment
    
    # Test storage access error
    os.chmod(storage_path, 0o000)  # Remove permissions
    with pytest.raises(TaskError):
        cli.handle_add_task()
    os.chmod(storage_path, 0o600)  # Restore permissions
    
    # Test task limit error
    for i in range(1001):  # Exceed 1000 task limit
        task = Task(id=i, description=f"Task {i}", status="pending")
        cli._task_manager._task_cache[task.id] = task
    
    mock_menu.display_task_input.return_value = "New task"
    with pytest.raises(TaskError):
        cli.handle_add_task()
    
    # Verify error recovery
    assert cli._running  # System remains operational
    assert cli._session_state['operations_performed'] > 0  # Operations tracked
    mock_menu.show_message.assert_called()  # Error message displayed