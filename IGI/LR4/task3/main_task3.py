"""
Main module for Task 3: Function approximation.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24
"""
from task3.function_approximator import FunctionApproximator
from utilities.input_utils import get_valid_int

def run_task3():
    """Run Task 3 with user input and plot the results."""
    print("=== Task 3: Function Approximation ===")
    num_points = get_valid_int("Enter number of points (10-100): ", 10, 100)
    n_terms = get_valid_int("Enter number of terms (1-20): ", 1, 20)
    approximator = FunctionApproximator(-1.0, 1.0, num_points, n_terms)
    for x, y in zip(approximator.x_values, approximator.approximations):
        print(f"x={x:.2f}, arccos(x)≈{y:.6f}")
    approximator.plot("arccos_plot.png")
    print("Plot saved as arccos_plot.png")