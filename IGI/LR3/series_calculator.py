# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

import math
from utils import get_float_input

def compute_arccos_series(x, eps, max_iterations=500):
    """
    Compute arccos(x) using its power series expansion.

    Args:
        x (float): The input value, must be between -1 and 1.
        eps (float): Precision of the calculation.
        max_iterations (int): Maximum number of iterations (default is 500).

    Returns:
        tuple: (computed value of arccos(x), number of terms, math.acos(x) value)
    """
    if not -1 <= x <= 1:
        raise ValueError("x must be between -1 and 1")

    result = math.pi / 2
    term = x
    n = 0
    terms_count = 1

    while abs(term) > eps and n < max_iterations - 1:
        coefficient = math.factorial(2 * n) / (4 ** n * (math.factorial(n) ** 2) * (2 * n + 1))
        term = -coefficient * (x ** (2 * n + 1))
        result += term
        n += 1
        terms_count += 1

    math_value = math.acos(x)
    return result, terms_count, math_value

def display_results(x, fx, n, math_fx, eps):
    """
    Display results in a table-like format.

    Args:
        x (float): Input value.
        fx (float): Computed value of the function.
        n (int): Number of terms used.
        math_fx (float): Value from math module.
        eps (float): Precision.
    """
    print(f"x: {x:.4f} | n: {n} | F(x): {fx:.6f} | Math F(x): {math_fx:.6f} | eps: {eps}")

def sum_sequence_last_digits():
    """
    Multiply the last digits of numbers until 0 is entered.

    Returns:
        int: Product of last digits.
    """
    total = 1  # Initialize to 1 for multiplication
    print("Enter numbers to multiply their last digits (0 to stop):")
    while True:
        num = int(get_float_input("Enter a number (0 to stop): "))
        if num == 0:
            break
        last_digit = abs(num) % 10
        print(f"Last digit of {num} is {last_digit}")
        total *= last_digit  # Multiply the last digit
    return total