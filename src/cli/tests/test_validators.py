"""
Unit tests for input validation functions in the Simple To-Do List application.

This module contains comprehensive test cases for validating task descriptions,
menu options, task numbers, and task data structures with strict type checking
and security validation.

Version: 1.0
"""

import pytest  # version: 6.0.0+
from datetime import datetime
from typing import Dict, Any

from ..core.validators import (
    validate_task_description,
    validate_menu_option,
    validate_task_number,
    validate_task_data
)
from ..types.custom_types import TaskDict
from ..exceptions.validation_exceptions import (
    ValidationError,
    TaskDescriptionValidationError,
    MenuOptionValidationError,
    TaskNumberValidationError
)

# Test data constants
VALID_TASK_DESCRIPTION = "Buy groceries"
VALID_UNICODE_DESCRIPTION = "Comprar víveres"
INVALID_TASK_DESCRIPTIONS = [
    None,
    "",
    " " * 5,
    "a" * 201,
    "Invalid@#$Characters",
    "\x00malicious",
    "<script>alert('xss')</script>",
    "../path/traversal",
    "DROP TABLE tasks;"
]

VALID_MENU_OPTIONS = ["1", "2", "3", "4"]
INVALID_MENU_OPTIONS = [
    None,
    "",
    "0",
    "5",
    "abc",
    "1.5",
    "-1",
    " ",
    "2 ",
    " 3",
    "\n4"
]

VALID_TASK_DATA = {
    "id": 1,
    "description": "Valid task",
    "status": "pending",
    "created": datetime(2024, 1, 1, 10, 0, 0),
    "modified": datetime(2024, 1, 1, 10, 0, 0)
}

INVALID_TASK_DATA_SAMPLES = [
    {},  # Empty dictionary
    {"id": "abc", "status": "pending"},  # Missing description
    {"id": 1, "description": "", "status": "unknown"},  # Invalid status
    {"id": -1, "description": "Valid", "status": "pending"},  # Invalid ID
    {"id": 1, "description": "Valid", "status": "pending", "created": "not-a-date"},
    {"description": "Valid", "status": "pending"},  # Missing ID
    {"id": 1, "description": None, "status": "pending"},  # None description
    {"id": 1, "description": "Valid", "status": None}  # None status
]

@pytest.mark.timeout(1)
def test_validate_task_description_valid():
    """Test validation of valid task descriptions."""
    assert validate_task_description(VALID_TASK_DESCRIPTION) is True
    assert validate_task_description(VALID_UNICODE_DESCRIPTION) is True
    assert validate_task_description("Task with numbers 123") is True
    assert validate_task_description("Task with punctuation!") is True

@pytest.mark.timeout(1)
@pytest.mark.parametrize("invalid_description", INVALID_TASK_DESCRIPTIONS)
def test_validate_task_description_invalid(invalid_description):
    """Test validation of invalid task descriptions."""
    with pytest.raises(TaskDescriptionValidationError) as exc_info:
        validate_task_description(invalid_description)
    assert exc_info.value.error_code == "E001"
    assert "[E001]" in str(exc_info.value)

@pytest.mark.timeout(1)
@pytest.mark.parametrize("valid_option", VALID_MENU_OPTIONS)
def test_validate_menu_option_valid(valid_option):
    """Test validation of valid menu options."""
    result = validate_menu_option(valid_option)
    assert isinstance(result, int)
    assert 1 <= result <= 4

@pytest.mark.timeout(1)
@pytest.mark.parametrize("invalid_option", INVALID_MENU_OPTIONS)
def test_validate_menu_option_invalid(invalid_option):
    """Test validation of invalid menu options."""
    with pytest.raises(MenuOptionValidationError) as exc_info:
        validate_menu_option(invalid_option)
    assert exc_info.value.error_code == "E002"
    assert "[E002]" in str(exc_info.value)

@pytest.mark.timeout(1)
def test_validate_task_number_valid():
    """Test validation of valid task numbers."""
    max_tasks = 5
    for i in range(1, max_tasks + 1):
        result = validate_task_number(str(i), max_tasks)
        assert isinstance(result, int)
        assert result == i

@pytest.mark.timeout(1)
@pytest.mark.parametrize("invalid_number", ["0", "6", "abc", "-1", "1.5", "", " "])
def test_validate_task_number_invalid(invalid_number):
    """Test validation of invalid task numbers."""
    max_tasks = 5
    with pytest.raises(TaskNumberValidationError) as exc_info:
        validate_task_number(invalid_number, max_tasks)
    assert exc_info.value.error_code == "E003"
    assert "[E003]" in str(exc_info.value)
    assert str(max_tasks) in str(exc_info.value)

def test_validate_task_data_valid():
    """Test validation of valid task data structure."""
    assert validate_task_data(VALID_TASK_DATA) is True

    # Test minimal valid task data
    minimal_task = {
        "id": 1,
        "description": "Valid task",
        "status": "pending"
    }
    assert validate_task_data(minimal_task) is True

@pytest.mark.timeout(1)
@pytest.mark.parametrize("invalid_data", INVALID_TASK_DATA_SAMPLES)
def test_validate_task_data_invalid(invalid_data):
    """Test validation of invalid task data structures."""
    with pytest.raises(ValidationError) as exc_info:
        validate_task_data(invalid_data)
    assert exc_info.value.error_code in ["E004", "E005", "E006", "E007", "E008", "E009"]
    assert "[E" in str(exc_info.value)

@pytest.mark.timeout(1)
def test_validate_task_data_type_safety():
    """Test type safety of task data validation."""
    # Test with incorrect types for each field
    type_error_cases = [
        {"id": 1.5, "description": "Valid", "status": "pending"},
        {"id": 1, "description": 123, "status": "pending"},
        {"id": 1, "description": "Valid", "status": True},
        {"id": 1, "description": "Valid", "status": "pending", "created": "invalid"}
    ]
    
    for invalid_data in type_error_cases:
        with pytest.raises(ValidationError) as exc_info:
            validate_task_data(invalid_data)
        assert exc_info.value.error_code in ["E006", "E007", "E008", "E009"]