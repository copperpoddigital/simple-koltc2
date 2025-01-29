"""
Utility module for handling command-line output formatting and display functions.
Provides consistent interface rendering, task display formatting, and message output
handling with cross-platform support and accessibility considerations.

Version: 1.0
"""

from typing import List, Optional  # Python 3.6+
import os
import shutil
from datetime import datetime

from ..constants.messages import (
    SUCCESS_MESSAGES,
    ERROR_MESSAGES,
    INFO_MESSAGES,
    MENU_MESSAGES
)
from ..constants.symbols import (
    NAVIGATION_SYMBOLS,
    STATUS_SYMBOLS,
    ACTION_SYMBOLS,
    BORDER_SYMBOLS,
    MENU_SYMBOLS
)
from ..models.task import Task

# Screen layout constants
SCREEN_WIDTH = 80
MENU_PADDING = 2
MAX_TASK_DESCRIPTION_LENGTH = 60
TASKS_PER_PAGE = 10

def clear_screen() -> None:
    """
    Clears the terminal screen in a cross-platform manner with fallback support.
    Handles different operating systems and terminal types safely.
    """
    try:
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Unix/Linux/MacOS
        else:
            os.system('clear')
    except Exception:
        # Fallback to printing newlines if system commands fail
        print('\n' * 100)

def print_header(title: str, show_navigation: bool = True) -> None:
    """
    Prints the application header with borders and optional navigation hints.

    Args:
        title (str): The title to display in the header
        show_navigation (bool): Whether to show navigation hints
    """
    # Create top border
    print(f"{BORDER_SYMBOLS['TOP_LEFT']}{BORDER_SYMBOLS['HORIZONTAL'] * (SCREEN_WIDTH - 2)}"
          f"{BORDER_SYMBOLS['TOP_RIGHT']}")
    
    # Center title
    padding = (SCREEN_WIDTH - len(title) - 2) // 2
    print(f"{BORDER_SYMBOLS['VERTICAL']}{' ' * padding}{title}"
          f"{' ' * (SCREEN_WIDTH - padding - len(title) - 2)}{BORDER_SYMBOLS['VERTICAL']}")
    
    # Add navigation hints if requested
    if show_navigation:
        nav_line = (f"{NAVIGATION_SYMBOLS['BACK']} Back "
                   f"{MENU_SYMBOLS['SEPARATOR']} "
                   f"{ACTION_SYMBOLS['HELP']} Help "
                   f"{MENU_SYMBOLS['SEPARATOR']} "
                   f"{NAVIGATION_SYMBOLS['ESCAPE']} Exit")
        nav_padding = (SCREEN_WIDTH - len(nav_line) - 2) // 2
        print(f"{BORDER_SYMBOLS['VERTICAL']}{' ' * nav_padding}{nav_line}"
              f"{' ' * (SCREEN_WIDTH - nav_padding - len(nav_line) - 2)}"
              f"{BORDER_SYMBOLS['VERTICAL']}")
    
    # Bottom border
    print(f"{BORDER_SYMBOLS['BOTTOM_LEFT']}{BORDER_SYMBOLS['HORIZONTAL'] * (SCREEN_WIDTH - 2)}"
          f"{BORDER_SYMBOLS['BOTTOM_RIGHT']}")

def format_task(task: Task, show_timestamps: bool = False) -> str:
    """
    Formats a single task for display with status indicator and truncation.

    Args:
        task (Task): The task to format
        show_timestamps (bool): Whether to include creation/modification timestamps

    Returns:
        str: Formatted task string with status, description, and optional timestamps
    """
    # Get status symbol
    status_symbol = STATUS_SYMBOLS['COMPLETED'] if task.status == 'completed' else STATUS_SYMBOLS['PENDING']
    
    # Format description with truncation if needed
    description = task.description
    if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
        description = f"{description[:MAX_TASK_DESCRIPTION_LENGTH-3]}..."
    
    # Basic task format
    formatted_task = f"{task.id:3d}. {status_symbol} {description}"
    
    # Add timestamps if requested
    if show_timestamps:
        created = task.created.strftime("%Y-%m-%d %H:%M")
        modified = task.modified.strftime("%Y-%m-%d %H:%M")
        formatted_task = f"{formatted_task:<{MAX_TASK_DESCRIPTION_LENGTH + 8}} Created: {created} Modified: {modified}"
    
    return formatted_task

def print_task_list(tasks: List[Task], page_number: int = 1, show_timestamps: bool = False) -> None:
    """
    Displays the list of tasks with pagination and statistics.

    Args:
        tasks (List[Task]): List of tasks to display
        page_number (int): Current page number (1-based)
        show_timestamps (bool): Whether to show task timestamps
    """
    # Calculate pagination
    total_pages = (len(tasks) + TASKS_PER_PAGE - 1) // TASKS_PER_PAGE
    start_idx = (page_number - 1) * TASKS_PER_PAGE
    end_idx = min(start_idx + TASKS_PER_PAGE, len(tasks))
    
    # Print header with page information
    print_header("Task List", show_navigation=True)
    if total_pages > 1:
        print(f"Page {page_number}/{total_pages}")
    
    # Handle empty task list
    if not tasks:
        print(f"\n{MENU_SYMBOLS['INDENT']}{INFO_MESSAGES['no_tasks']}\n")
        return
    
    # Print tasks for current page
    print()  # Empty line for spacing
    for task in tasks[start_idx:end_idx]:
        print(f"{MENU_SYMBOLS['INDENT']}{format_task(task, show_timestamps)}")
    print()  # Empty line for spacing
    
    # Print task statistics
    completed_count = sum(1 for task in tasks if task.status == 'completed')
    print(INFO_MESSAGES['task_count'].format(
        len(tasks), completed_count, len(tasks) - completed_count))
    
    # Show pagination navigation hints if multiple pages
    if total_pages > 1:
        print(f"\n{NAVIGATION_SYMBOLS['BACK']}/{NAVIGATION_SYMBOLS['FORWARD']} "
              f"Navigate pages | {NAVIGATION_SYMBOLS['RETURN']} Select")

def print_message(message: str, message_type: str = 'info', use_border: bool = False) -> None:
    """
    Prints a formatted message with appropriate styling and symbols.

    Args:
        message (str): The message to display
        message_type (str): Type of message ('success', 'error', 'info', 'warning')
        use_border (bool): Whether to add borders around the message
    """
    # Select appropriate symbol based on message type
    symbols = {
        'success': STATUS_SYMBOLS['SUCCESS'],
        'error': STATUS_SYMBOLS['ERROR'],
        'info': STATUS_SYMBOLS['INFO'],
        'warning': STATUS_SYMBOLS['WARNING']
    }
    symbol = symbols.get(message_type, STATUS_SYMBOLS['INFO'])
    
    # Format message with symbol
    formatted_message = f"{symbol} {message}"
    
    # Add borders if requested
    if use_border:
        width = min(len(formatted_message) + 4, SCREEN_WIDTH)
        print(f"{BORDER_SYMBOLS['TOP_LEFT']}{BORDER_SYMBOLS['HORIZONTAL'] * (width - 2)}"
              f"{BORDER_SYMBOLS['TOP_RIGHT']}")
        print(f"{BORDER_SYMBOLS['VERTICAL']} {formatted_message}"
              f"{' ' * (width - len(formatted_message) - 4)} {BORDER_SYMBOLS['VERTICAL']}")
        print(f"{BORDER_SYMBOLS['BOTTOM_LEFT']}{BORDER_SYMBOLS['HORIZONTAL'] * (width - 2)}"
              f"{BORDER_SYMBOLS['BOTTOM_RIGHT']}")
    else:
        print(formatted_message)