"""
Drawing functionality for Task 4.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module provides functions to draw geometric figures using matplotlib.
"""
import matplotlib.pyplot as plt

def draw_trapezoid(trap, text):
    """Draw the trapezoid using matplotlib.

    Args:
        trap (Trapezoid): The trapezoid object to draw.
        text (str): Text to label the figure.
    """
    a, c, h = trap.base_a, trap._c, trap.height
    offset = (a - c) / 2

    # Coordinates of trapezoid vertices
    x = [0, a, a - offset, offset, 0]
    y = [0, 0, h, h, 0]

    plt.figure(figsize=(6, 4))
    plt.fill(x, y, color=trap.color, edgecolor='black')
    plt.text(a / 2, -h * 0.1, text, ha='center', fontsize=12)
    plt.axis('equal')
    plt.axis('off')
    filename = f"{text.lower()}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.show()
    print(f"Figure saved as {filename}")