# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

from datetime import datetime  # Import datetime for measuring execution time

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
    Decorator to allow repeated execution of a function with logging.

    This decorator:
    - Allows the function to be repeated based on user input.
    - Logs the function name, arguments, start time, end time, and execution time.

    Args:
        func: The function to decorate.

    Returns:
        function: Wrapped function with repeat and logging logic.
    """
    def wrapper(*args, **kwargs):
        while True:
            # Log the start of the function execution
            start_time = datetime.now()
            print(f"Calling function {func.__name__} at {start_time} with arguments: {args}, keyword arguments: {kwargs}")

            # Execute the function
            func(*args, **kwargs)

            # Log the end of the function execution
            end_time = datetime.now()
            print(f"Function {func.__name__} completed at {end_time}")

            # Calculate and log the execution time
            execution_time = end_time - start_time
            print(f"Function execution time: {execution_time.total_seconds()} seconds")

            choice = input("Do you want to continue? (yes/no): ").lower()
            if choice != 'yes':
                break

    return wrapper