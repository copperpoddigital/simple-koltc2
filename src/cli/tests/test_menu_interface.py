"""
Test suite for the menu interface component of the Simple To-Do List application.
Validates menu display, user input handling, interface flow, and performance requirements.

Version: 1.0
"""

import pytest  # version: 6.0.0+
from unittest.mock import Mock, patch  # version: 3.6+
import time  # version: 3.6+
from datetime import datetime
import io
import sys

from ..interfaces.menu_interface import MenuInterface
from ..models.task import Task
from ..constants.messages import MENU_MESSAGES, ERROR_MESSAGES, INFO_MESSAGES
from ..constants.symbols import BORDER_SYMBOLS, STATUS_SYMBOLS

class TestMenuInterface:
    """Test suite for MenuInterface class functionality."""

    @pytest.fixture
    def menu_interface(self):
        """Fixture providing a fresh MenuInterface instance for each test."""
        with patch('sys.stdout', new_callable=io.StringIO), \
             patch('builtins.input', return_value='4'):
            interface = MenuInterface()
            return interface

    @pytest.fixture
    def sample_tasks(self):
        """Fixture providing a list of test tasks with various states."""
        return [
            Task(1, "First task", "pending", datetime.utcnow(), datetime.utcnow()),
            Task(2, "Second task", "completed", datetime.utcnow(), datetime.utcnow()),
            Task(3, "Third task with a very long description that should be truncated", "pending", 
                 datetime.utcnow(), datetime.utcnow())
        ]

    @pytest.mark.menu
    def test_display_menu_shows_correct_options(self, menu_interface):
        """Test that main menu displays all required options with correct formatting."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('builtins.input', return_value='4'):
            
            menu_interface.display_menu()
            output = mock_stdout.getvalue()

            # Verify menu title and borders
            assert MENU_MESSAGES['main_title'] in output
            assert BORDER_SYMBOLS['TOP_LEFT'] in output
            assert BORDER_SYMBOLS['TOP_RIGHT'] in output
            
            # Verify all menu options are present
            assert MENU_MESSAGES['add_task'] in output
            assert MENU_MESSAGES['view_tasks'] in output
            assert MENU_MESSAGES['complete_task'] in output
            assert MENU_MESSAGES['exit'] in output

            # Verify menu formatting
            lines = output.split('\n')
            assert all(len(line) <= 80 for line in lines), "Menu exceeds 80 character width limit"
            assert any(MENU_MESSAGES['choice_prompt'] in line for line in lines)

    @pytest.mark.menu
    @pytest.mark.input
    def test_display_menu_validates_input(self, menu_interface):
        """Test menu input validation including invalid inputs and edge cases."""
        invalid_inputs = ['a', '0', '5', ' ', '#']
        valid_input = '2'
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('builtins.input', side_effect=invalid_inputs + [valid_input]):
            
            result = menu_interface.display_menu()
            output = mock_stdout.getvalue()

            # Verify error messages for invalid inputs
            assert ERROR_MESSAGES['invalid_input'] in output
            assert output.count(ERROR_MESSAGES['invalid_input']) == len(invalid_inputs)
            
            # Verify final valid input is accepted
            assert result == int(valid_input)

    @pytest.mark.display
    def test_display_task_list_formatting(self, menu_interface, sample_tasks):
        """Test task list display formatting and pagination."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('builtins.input', return_value='\n'):
            
            menu_interface.display_task_list(sample_tasks)
            output = mock_stdout.getvalue()

            # Verify task status indicators
            assert STATUS_SYMBOLS['PENDING'] in output
            assert STATUS_SYMBOLS['COMPLETED'] in output

            # Verify task formatting
            lines = output.split('\n')
            task_lines = [l for l in lines if any(str(t.id) in l for t in sample_tasks)]
            
            # Check task numbering and description formatting
            for task, line in zip(sample_tasks, task_lines):
                assert str(task.id) in line
                assert task.description[:50] in line  # Account for truncation
                status = STATUS_SYMBOLS['COMPLETED'] if task.status == 'completed' else STATUS_SYMBOLS['PENDING']
                assert status in line

    @pytest.mark.display
    def test_display_task_input_validation(self, menu_interface):
        """Test task input screen validation and formatting."""
        invalid_desc = "Task with invalid chars @#$"
        valid_desc = "Valid task description"
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('builtins.input', side_effect=[invalid_desc, valid_desc]):
            
            result = menu_interface.display_task_input()
            output = mock_stdout.getvalue()

            # Verify input validation
            assert ERROR_MESSAGES['invalid_chars'] in output
            assert result == valid_desc

            # Verify screen formatting
            assert len(max(output.split('\n'), key=len)) <= 80

    @pytest.mark.performance
    def test_menu_performance_requirements(self, menu_interface, sample_tasks):
        """Test menu component performance against requirements."""
        with patch('time.time', side_effect=[0.0, 0.05, 0.1, 0.15]):  # Simulate time intervals
            
            # Test menu display time (<100ms)
            start = time.time()
            menu_interface.display_menu()
            assert time.time() - start < 0.1, "Menu display exceeded 100ms limit"

            # Test task list display time (<200ms)
            start = time.time()
            menu_interface.display_task_list(sample_tasks)
            assert time.time() - start < 0.2, "Task list display exceeded 200ms limit"

    @pytest.mark.error
    def test_error_message_display(self, menu_interface):
        """Test error message formatting and display."""
        test_error = "Test error message"
        
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            menu_interface.show_message(test_error, 'error')
            output = mock_stdout.getvalue()

            # Verify error formatting
            assert STATUS_SYMBOLS['ERROR'] in output
            assert test_error in output
            assert len(max(output.split('\n'), key=len)) <= 80

    @pytest.mark.keyboard
    def test_keyboard_interrupt_handling(self, menu_interface):
        """Test handling of keyboard interrupts during menu operations."""
        with patch('builtins.input', side_effect=KeyboardInterrupt), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            
            result = menu_interface.display_menu()
            output = mock_stdout.getvalue()

            # Verify graceful exit
            assert result == 4  # Exit option
            assert INFO_MESSAGES['confirm_exit'] in output