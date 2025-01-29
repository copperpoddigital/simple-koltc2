"""
Menu interface component for the Simple To-Do List application.

Implements secure and robust menu-based user interface functionality with comprehensive
error handling, input validation, and consistent layout formatting according to technical specifications.

Version: 1.0
"""

from typing import List, Optional, Dict, Any  # version: 3.6+

from ..models.task import Task
from ..utils.output_utils import (
    clear_screen,
    print_header,
    print_task_list,
    print_message,
    wait_for_enter
)
from ..utils.input_utils import (
    get_menu_option,
    get_task_description,
    get_task_number,
    validate_input
)
from ..constants.messages import (
    SUCCESS_MESSAGES,
    ERROR_MESSAGES,
    INFO_MESSAGES,
    MENU_MESSAGES
)

# Interface configuration constants
APP_TITLE = "Simple To-Do List App"
MAX_DISPLAY_TASKS = 10
INPUT_TIMEOUT = 30  # seconds

class MenuInterface:
    """
    Handles menu-related display and interaction functionality with comprehensive
    security and error handling.
    """
    
    def __init__(self) -> None:
        """Initialize menu interface with secure state management."""
        self._current_page = 1
        self._total_pages = 1
        self._session_state: Dict[str, Any] = {
            'last_action': None,
            'input_buffer': '',
            'display_mode': 'normal'
        }
        
        # Clear screen and initialize interface
        clear_screen()
        print_header(APP_TITLE)
        print_message(INFO_MESSAGES['welcome'], 'info')
    
    @property
    def current_page(self) -> int:
        """Get current page number with bounds checking."""
        return max(1, min(self._current_page, self._total_pages))
    
    @property
    def total_pages(self) -> int:
        """Get total number of pages."""
        return max(1, self._total_pages)
    
    def display_menu(self) -> int:
        """
        Display main menu and securely get user selection.
        
        Returns:
            int: Validated menu option (1-4)
        """
        try:
            clear_screen()
            print_header(APP_TITLE)
            
            # Display menu options
            for message in [
                MENU_MESSAGES['add_task'],
                MENU_MESSAGES['view_tasks'],
                MENU_MESSAGES['complete_task'],
                MENU_MESSAGES['exit']
            ]:
                print(message)
            
            print(MENU_MESSAGES['divider'])
            
            # Get and validate user input
            return get_menu_option()
            
        except KeyboardInterrupt:
            print_message(INFO_MESSAGES['confirm_exit'], 'info')
            return 4  # Exit option
        except Exception as e:
            print_message(str(e), 'error')
            return self.display_menu()
    
    def display_task_input(self) -> str:
        """
        Display task input screen with secure input handling.
        
        Returns:
            str: Sanitized and validated task description
        """
        try:
            clear_screen()
            print_header("Add New Task")
            
            # Display input guidelines
            print("Guidelines:")
            print("- Maximum 200 characters")
            print("- Alphanumeric characters and basic punctuation only")
            print("- Press [Enter] to submit, [Esc] to cancel")
            print(MENU_MESSAGES['divider'])
            
            # Get and validate task description
            return get_task_description()
            
        except KeyboardInterrupt:
            return ''
        except Exception as e:
            print_message(str(e), 'error')
            return self.display_task_input()
    
    def display_task_list(self, tasks: List[Task], page_number: Optional[int] = None) -> None:
        """
        Display paginated list of tasks with security checks.
        
        Args:
            tasks: List[Task]: Tasks to display
            page_number: Optional[int]: Page number to display
        """
        try:
            # Update pagination state
            self._total_pages = (len(tasks) + MAX_DISPLAY_TASKS - 1) // MAX_DISPLAY_TASKS
            if page_number is not None:
                self._current_page = max(1, min(page_number, self._total_pages))
            
            clear_screen()
            print_task_list(tasks, self.current_page)
            wait_for_enter()
            
        except Exception as e:
            print_message(str(e), 'error')
            wait_for_enter()
    
    def display_completion_menu(self, tasks: List[Task]) -> int:
        """
        Display task completion menu with secure selection.
        
        Args:
            tasks: List[Task]: Available tasks
            
        Returns:
            int: Validated task ID
        """
        try:
            clear_screen()
            print_header("Mark Task as Complete")
            
            # Display only pending tasks
            pending_tasks = [task for task in tasks if not task.completed]
            if not pending_tasks:
                print_message(INFO_MESSAGES['no_tasks'], 'info')
                wait_for_enter()
                return 0
            
            print_task_list(pending_tasks)
            print(MENU_MESSAGES['divider'])
            
            # Get and validate task selection
            return get_task_number(len(pending_tasks))
            
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            print_message(str(e), 'error')
            return self.display_completion_menu(tasks)
    
    def show_message(self, message: str, message_type: str = 'info',
                    wait_for_input: bool = True) -> None:
        """
        Display sanitized message with appropriate styling.
        
        Args:
            message: str: Message to display
            message_type: str: Type of message ('success', 'error', 'info', 'warning')
            wait_for_input: bool: Whether to wait for user acknowledgment
        """
        try:
            print_message(message, message_type)
            if wait_for_input:
                wait_for_enter()
                
        except Exception as e:
            # Fallback to basic print if formatting fails
            print(f"[!] {str(e)}")
            if wait_for_input:
                input(INFO_MESSAGES['press_enter'])