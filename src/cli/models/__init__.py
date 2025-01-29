"""
Models package initialization for the Simple To-Do List application.

This package provides access to the core data models used throughout the application,
with a focus on type safety, validation, and secure data handling.

Version: 1.0
"""

# Re-export Task class for clean package-level access
from .task import Task

# Define package exports
__all__ = ['Task']