"""
Main module for Task 4: Geometric figures.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module provides the main function to run Task 4, allowing the user to create and draw trapezoids.
"""
from task4.trapezoid import Trapezoid
from task4.drawer import draw_trapezoid
from utilities.input_utils import get_valid_float

def run_task4():
    """Run Task 4 with a user-friendly interface to draw trapezoids."""
    print("=== Task 4: Drawing Trapezoids ===")
    print("You will create and draw a Trapezoid.")
    while True:
        try:
            h = get_valid_float("Enter trapezoid height (positive number): ", 0.1)
            a = get_valid_float("Enter trapezoid base a (positive number): ", 0.1)
            min_b = a / 2 + 0.1
            b = get_valid_float(f"Enter trapezoid middle line b (must be > {min_b:.1f}): ", min_b)
            color = input("Enter trapezoid color (e.g., blue, red): ")
            trap = Trapezoid(h, a, b, color)
            print(f"Created: {trap}")
            draw_trapezoid(trap, "Trapezoid")
            if input("Draw another trapezoid? (y/n): ").lower() != 'y':
                break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")