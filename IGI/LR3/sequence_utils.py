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
    Initialize a list with random numbers.

    Args:
        size (int): Number of elements in the list.

    Returns:
        list: List of random floats.
    """
    return [random.uniform(-10, 10) for _ in range(size)]

def process_list(sequence):
    """
    Find max element index and product between first two non-zero elements.

    Args:
        sequence (list): List of floats.

    Returns:
        tuple: (max_index, product)
    """
    max_index = sequence.index(max(sequence))
    non_zeros = [x for x in sequence if x != 0]
    product = non_zeros[0] * non_zeros[1] if len(non_zeros) >= 2 else 0
    return max_index, product