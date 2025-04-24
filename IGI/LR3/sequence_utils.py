# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

from utils import get_float_input
import random

def initialize_with_input(size):
    """
    Initialize a list with user input.

    Args:
        size (int): Number of elements in the list.

    Returns:
        list: List of floats entered by the user.
    """
    sequence = []
    for i in range(size):
        value = get_float_input(f"Enter element {i + 1}: ")
        sequence.append(value)
    return sequence

def initialize_with_generator(size):
    """
    Generate a sequence of random numbers using yield.

    Args:
        size (int): Number of elements in the sequence.

    Yields:
        float: Random float between -10 and 10.
    """
    for _ in range(size):
        yield random.uniform(-10, 10)

def process_list(sequence):
    """
    Find max element index and product between first two non-zero elements.

    Args:
        sequence (list): List of floats.

    Returns:
        tuple: (max_index, product)

    Raises:
        ValueError: If the list has fewer than two non-zero elements or is empty.
    """
    if not sequence:
        raise ValueError("List cannot be empty")
    max_index = sequence.index(max(sequence))
    non_zeros = [x for x in sequence if x != 0]
    if len(non_zeros) < 2:
        raise ValueError("List must contain at least two non-zero elements for product calculation")
    product = non_zeros[0] * non_zeros[1]
    return max_index, product