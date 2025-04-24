"""
Utility functions for input validation.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24
"""

def get_valid_int(prompt, min_val=None, max_val=None):
    """Get a valid integer input from the user.

    Args:
        prompt (str): The prompt to display.
        min_val (int, optional): Minimum allowed value.
        max_val (int, optional): Maximum allowed value.

    Returns:
        int: Validated integer.

    Raises:
        ValueError: If input is invalid or out of range.
    """
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError(f"Value must be between {min_val} and {max_val}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def get_valid_float(prompt, min_val=None, max_val=None):
    """Get a valid float input from the user.

    Args:
        prompt (str): The prompt to display.
        min_val (float, optional): Minimum allowed value.
        max_val (float, optional): Maximum allowed value.

    Returns:
        float: Validated float.

    Raises:
        ValueError: If input is invalid or out of range.
    """
    while True:
        try:
            value = float(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError(f"Value must be between {min_val} and {max_val}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")