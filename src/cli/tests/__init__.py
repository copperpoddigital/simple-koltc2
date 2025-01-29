"""
Test package initialization module for the Simple To-Do List application.

This module exposes testing utilities, fixtures, and configuration for automated testing,
providing centralized access to commonly used test components and ensuring proper test
environment setup for CI/CD pipeline integration.

Version: 1.0
Python: 3.6+
"""

# pytest version: 6.0.0+
from .conftest import (
    temp_storage_path,
    task_storage,
    task_manager,
    sample_tasks
)

# Export fixtures for test suite usage
__all__ = [
    "temp_storage_path",  # Provides temporary file system path for isolated test storage
    "task_storage",       # Provides TaskStorage instance for data persistence
    "task_manager",       # Provides TaskManager instance for task operations
    "sample_tasks"        # Provides predefined task data for test scenarios
]

# Ensure fixtures are properly registered with pytest
def pytest_configure(config):
    """
    Register custom markers and configure test environment.
    
    Args:
        config: pytest configuration object
    """
    config.addinivalue_line(
        "markers",
        "storage: mark test as requiring storage fixture"
    )
    config.addinivalue_line(
        "markers",
        "manager: mark test as requiring task manager fixture"
    )
    config.addinivalue_line(
        "markers",
        "samples: mark test as requiring sample tasks fixture"
    )