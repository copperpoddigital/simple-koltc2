"""
Main command-line interface component for the Simple To-Do List application.

Orchestrates user interaction, menu system, and task management with comprehensive
error handling, security measures, and performance monitoring.

Version: 1.0
Python: 3.6+
"""

import sys  # version: 3.6+
import time  # version: 3.6+
from typing import Dict, Any, Optional  # version: 3.6+

from ..core.task_manager import TaskManager, TaskValidationError, TaskStorageError
from .menu_interface import MenuInterface

# Performance thresholds in milliseconds
MENU_RESPONSE_THRESHOLD = 100
OPERATION_TIMEOUT = 500

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

class CLIInterface:
    """
    Main CLI interface class that coordinates user interaction and task management
    with enhanced security, error handling, and performance monitoring.
    """

    def __init__(self, storage_path: str) -> None:
        """
        Initialize CLI interface with task manager, menu interface, and monitoring systems.

        Args:
            storage_path: Path to task storage file
        """
        # Initialize core components
        self._task_manager = TaskManager(storage_path)
        self._menu_interface = MenuInterface()
        self._running = False

        # Initialize monitoring
        self._performance_metrics: Dict[str, float] = {
            'menu_response': 0.0,
            'task_operations': 0.0,
            'total_runtime': 0.0
        }

        # Initialize session state
        self._session_state: Dict[str, Any] = {
            'tasks_added': 0,
            'tasks_completed': 0,
            'operations_performed': 0,
            'last_operation': None
        }

    def run(self) -> int:
        """
        Main application loop with enhanced error handling and performance monitoring.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        self._running = True
        start_time = time.time()

        try:
            while self._running:
                # Start operation timer
                operation_start = time.time()

                # Display menu and get user choice
                choice = self._menu_interface.display_menu()
                menu_response_time = (time.time() - operation_start) * 1000

                # Monitor menu response time
                if menu_response_time > MENU_RESPONSE_THRESHOLD:
                    self._performance_metrics['menu_response'] = menu_response_time

                # Handle menu selection
                try:
                    if choice == 1:
                        self.handle_add_task()
                    elif choice == 2:
                        self.handle_view_tasks()
                    elif choice == 3:
                        self.handle_complete_task()
                    elif choice == 4:
                        self.handle_exit()

                    # Update session state
                    self._session_state['operations_performed'] += 1
                    self._session_state['last_operation'] = choice

                except TaskValidationError as e:
                    self._menu_interface.show_message(str(e), 'error')
                except TaskStorageError as e:
                    self._menu_interface.show_message(str(e), 'error')
                except Exception as e:
                    self._menu_interface.show_message(f"An error occurred: {str(e)}", 'error')

            # Record total runtime
            self._performance_metrics['total_runtime'] = time.time() - start_time
            return EXIT_SUCCESS

        except KeyboardInterrupt:
            self.handle_exit()
            return EXIT_SUCCESS
        except Exception as e:
            self._menu_interface.show_message(f"Fatal error: {str(e)}", 'error')
            return EXIT_FAILURE

    def handle_add_task(self) -> None:
        """
        Handle task addition workflow with input validation and error handling.
        """
        operation_start = time.time()

        try:
            # Get task description from user
            description = self._menu_interface.display_task_input()
            if not description:  # User cancelled
                return

            # Create task
            task = self._task_manager.create_task(description)
            
            # Update metrics
            operation_time = (time.time() - operation_start) * 1000
            self._performance_metrics['task_operations'] = operation_time
            self._session_state['tasks_added'] += 1

            # Show success message
            self._menu_interface.show_message("Task added successfully", 'success')

        except Exception as e:
            raise TaskValidationError(f"Failed to add task: {str(e)}")

    def handle_view_tasks(self) -> None:
        """
        Handle task viewing workflow with performance monitoring.
        """
        operation_start = time.time()

        try:
            # Get all tasks
            tasks = self._task_manager.get_all_tasks()
            
            # Display tasks
            self._menu_interface.display_task_list(tasks)

            # Update metrics
            operation_time = (time.time() - operation_start) * 1000
            self._performance_metrics['task_operations'] = operation_time

        except Exception as e:
            raise TaskStorageError(f"Failed to retrieve tasks: {str(e)}")

    def handle_complete_task(self) -> None:
        """
        Handle task completion workflow with validation and error handling.
        """
        operation_start = time.time()

        try:
            # Get all tasks
            tasks = self._task_manager.get_all_tasks()
            if not tasks:
                self._menu_interface.show_message("No tasks available", 'info')
                return

            # Get task selection from user
            task_number = self._menu_interface.display_completion_menu(tasks)
            if task_number == 0:  # User cancelled
                return

            # Complete selected task
            self._task_manager.complete_task(task_number)
            
            # Update metrics
            operation_time = (time.time() - operation_start) * 1000
            self._performance_metrics['task_operations'] = operation_time
            self._session_state['tasks_completed'] += 1

            # Show success message
            self._menu_interface.show_message("Task marked as complete", 'success')

        except Exception as e:
            raise TaskValidationError(f"Failed to complete task: {str(e)}")

    def handle_exit(self) -> None:
        """
        Handle application exit with cleanup.
        """
        self._running = False
        
        # Save final metrics
        self._performance_metrics['total_runtime'] = time.time() - time.time()
        
        # Show exit message
        self._menu_interface.show_message("Thank you for using Simple To-Do List App", 'info')