"""
Defines constant symbol dictionaries for visual elements used in the command-line interface formatting.
Includes navigation symbols, status indicators, action symbols, border characters, and menu formatting
symbols for consistent UI presentation across the application.
"""

from typing import Dict

# Navigation symbols used for menu traversal and interface flow control
NAVIGATION_SYMBOLS: Dict[str, str] = {
    'BACK': '[<]',      # Return to previous menu
    'FORWARD': '[>]',   # Proceed to next menu
    'UP': '[^]',        # Navigate upward/return to main
    'DOWN': '[v]',      # Navigate downward/show more
    'RETURN': '[Enter]', # Confirm/submit action
    'ESCAPE': '[Esc]',  # Cancel/exit current operation
    'CONTINUE': '...',  # Indicates more content
    'PAGE': 'Page'      # Page indicator prefix
}

# Status symbols for task and message state representation
STATUS_SYMBOLS: Dict[str, str] = {
    'PENDING': '[ ]',   # Uncompleted task
    'COMPLETED': '[x]', # Completed task
    'ERROR': '[!]',     # Error message indicator
    'INFO': '[i]',      # Information message indicator
    'WARNING': '[⚠]',   # Warning message indicator
    'SUCCESS': '[✓]'    # Success message indicator
}

# Action symbols for interactive interface elements
ACTION_SYMBOLS: Dict[str, str] = {
    'ADD': '[+]',       # Add new item
    'REMOVE': '[-]',    # Remove item
    'MENU': '[#]',      # Menu options
    'SETTINGS': '[=]',  # Settings/configuration
    'HELP': '[?]',      # Help/documentation
    'SAVE': '[💾]',     # Save changes
    'EDIT': '[✎]'      # Edit item
}

# Border characters for UI layout construction
BORDER_SYMBOLS: Dict[str, str] = {
    'TOP_LEFT': '+',     # Corner piece ┌
    'TOP_RIGHT': '+',    # Corner piece ┐
    'BOTTOM_LEFT': '+',  # Corner piece └
    'BOTTOM_RIGHT': '+', # Corner piece ┘
    'HORIZONTAL': '-',   # Horizontal line ─
    'VERTICAL': '|',     # Vertical line │
    'INTERSECTION': '+', # Cross intersection ┼
    'T_TOP': '+',        # T-piece ┬
    'T_BOTTOM': '+',     # T-piece ┴
    'T_LEFT': '+',       # T-piece ├
    'T_RIGHT': '+'       # T-piece ┤
}

# Menu formatting symbols for visual hierarchy
MENU_SYMBOLS: Dict[str, str] = {
    'OPTION': '•',      # Menu option bullet point
    'PROMPT': '>',      # Input prompt indicator
    'SEPARATOR': '|',   # Visual element separator
    'BULLET': '•',      # Generic bullet point
    'ARROW': '→',      # Direction/selection indicator
    'INDENT': '  '      # Standard indentation spacing
}