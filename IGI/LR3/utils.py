# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

def get_float_input(prompt):
    """
    Get a float input from the user with validation.

    Args:
        prompt (str): Message to display to the user.

    Returns:
        float: Validated float value.
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")

def repeat_execution(func):
    """
    Decorator to allow repeated execution of a function.

    Args:
        func: The function to decorate.

    Returns:
        function: Wrapped function with repeat logic.
    """
    def wrapper():
        while True:
            func()
            choice = input("Do you want to continue? (yes/no): ").lower()
            if choice != 'yes':
                break
    return wrapper