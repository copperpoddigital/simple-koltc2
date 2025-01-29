"""
Custom type definitions for the Simple To-Do List application.

This module defines type aliases and type hints used throughout the application
for type safety and validation. The types defined here match the JSON data structure
specification for tasks and metadata.

Version: 1.0
"""

from typing import TypeVar, TypeAlias, Literal, Dict, Union, List  # Python 3.6+
from datetime import datetime

# Type variable for task IDs that can be either integer or string
TaskId = TypeVar('TaskId', int, str)

# Literal type for constraining task status values
TaskStatus = Literal['pending', 'completed']

# Type alias for a task dictionary matching JSON schema
TaskDict: TypeAlias = Dict[str, Union[
    TaskId,          # id field
    str,            # description field
    TaskStatus,     # status field
    datetime        # created and modified fields
]]

# Type alias for a list of task dictionaries
TaskList: TypeAlias = List[TaskDict]

# Type alias for metadata dictionary matching JSON schema
MetadataDict: TypeAlias = Dict[str, Union[
    str,            # version field
    datetime,       # last_modified field
    int             # task_count field
]]