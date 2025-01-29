"""
Task model class for the Simple To-Do List application.

This module implements the Task class representing individual tasks with comprehensive
validation, secure data handling, and timestamp management according to the technical specification.

Version: 1.0
"""

from datetime import datetime
from dataclasses import dataclass
import re

from ..types.custom_types import TaskId, TaskStatus, TaskDict
from ..exceptions.task_exceptions import TaskValidationError

@dataclass
class Task:
    """
    Represents a single task in the to-do list with comprehensive validation and secure data handling.
    
    Attributes:
        id (TaskId): Unique identifier for the task
        description (str): Task description (1-200 characters)
        status (TaskStatus): Current task status ('pending' or 'completed')
        created (datetime): UTC timestamp of task creation
        modified (datetime): UTC timestamp of last modification
    """
    
    id: TaskId
    description: str
    status: TaskStatus
    created: datetime
    modified: datetime
    
    def __init__(
        self,
        id: TaskId,
        description: str,
        status: TaskStatus = 'pending',
        created: datetime = None,
        modified: datetime = None
    ) -> None:
        """
        Initialize a new task with validation and secure defaults.
        
        Args:
            id (TaskId): Unique task identifier
            description (str): Task description
            status (TaskStatus, optional): Task status. Defaults to 'pending'
            created (datetime, optional): Creation timestamp. Defaults to current UTC
            modified (datetime, optional): Modification timestamp. Defaults to created time
            
        Raises:
            TaskValidationError: If any validation checks fail
        """
        # Set timestamps with secure defaults
        self.created = created or datetime.utcnow()
        self.modified = modified or self.created
        
        # Assign and validate core properties
        self.id = id
        self.description = description
        self.status = status
        
        # Perform comprehensive validation
        self.validate()
    
    def validate(self) -> bool:
        """
        Perform comprehensive validation of task data with secure error handling.
        
        Returns:
            bool: True if all validations pass
            
        Raises:
            TaskValidationError: If any validation checks fail
        """
        # Validate ID
        if self.id is None:
            raise TaskValidationError("Task ID cannot be None")
        if not isinstance(self.id, (int, str)):
            raise TaskValidationError("Task ID must be integer or string")
            
        # Validate description
        if not isinstance(self.description, str):
            raise TaskValidationError("Description must be a string")
        if not 1 <= len(self.description) <= 200:
            raise TaskValidationError("Description must be between 1 and 200 characters")
        if not re.match(r'^[\w\s.,!?-]+$', self.description):
            raise TaskValidationError("Description contains invalid characters")
            
        # Validate status
        if self.status not in ('pending', 'completed'):
            raise TaskValidationError("Invalid task status")
            
        # Validate timestamps
        if self.created > datetime.utcnow():
            raise TaskValidationError("Creation time cannot be in the future")
        if self.modified < self.created:
            raise TaskValidationError("Modified time cannot be before creation time")
            
        return True
    
    def to_dict(self) -> TaskDict:
        """
        Convert task to dictionary with secure data handling.
        
        Returns:
            TaskDict: Secure dictionary representation of task
        """
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'created': self.created.isoformat(),
            'modified': self.modified.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: TaskDict) -> 'Task':
        """
        Create task from dictionary with validation.
        
        Args:
            data (TaskDict): Dictionary containing task data
            
        Returns:
            Task: New validated task instance
            
        Raises:
            TaskValidationError: If dictionary data is invalid
        """
        required_fields = {'id', 'description', 'status', 'created', 'modified'}
        if not all(field in data for field in required_fields):
            raise TaskValidationError("Missing required fields in task data")
            
        try:
            # Parse timestamps from ISO format
            created = datetime.fromisoformat(data['created'])
            modified = datetime.fromisoformat(data['modified'])
            
            # Create and validate new task instance
            return cls(
                id=data['id'],
                description=data['description'],
                status=data['status'],
                created=created,
                modified=modified
            )
        except (ValueError, TypeError) as e:
            raise TaskValidationError(f"Invalid task data format: {str(e)}")
    
    def mark_complete(self) -> None:
        """
        Mark task as completed with timestamp update.
        
        Updates the task status to completed and sets the modified timestamp
        to the current UTC time.
        """
        self.status = 'completed'
        self.modified = datetime.utcnow()
        self.validate()