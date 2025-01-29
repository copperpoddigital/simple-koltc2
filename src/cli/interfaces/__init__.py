"""
Initializes the interfaces package and exports the main interface components for the Simple To-Do List application.

This module provides a clean API for accessing the CLI and menu interfaces while maintaining
encapsulation and type safety. It exports only the necessary interface classes for external use
while keeping implementation details private.

Version: 1.0
Python: 3.6+
"""

from .cli_interface import CLIInterface
from .menu_interface import MenuInterface

# Package version
__version__ = "1.0.0"

# Explicitly define public exports
__all__ = [
    "CLIInterface",
    "MenuInterface"
]