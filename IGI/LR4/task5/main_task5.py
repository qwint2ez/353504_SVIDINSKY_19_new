"""
Main module for Task 5: Matrix analysis.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24
"""
from task5.matrix_analyzer import MatrixAnalyzer
from utilities.input_utils import get_valid_int

def run_task5():
    """Run Task 5 with user input."""
    print("=== Task 5: Matrix Analysis ===")
    n = get_valid_int("Matrix rows (1-10): ", 1, 10)
    m = get_valid_int("Matrix cols (1-10): ", 1, 10)
    analyzer = MatrixAnalyzer(n, m)
    results = analyzer.analyze()
    for k, v in results.items():
        print(f"{k}: {v}")