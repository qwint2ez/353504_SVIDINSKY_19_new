"""
FunctionApproximator class for Task 3: Approximate arccos(x).
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24

This module defines the FunctionApproximator class for function approximation.
"""
import math
import numpy as np
from abc import ABC, abstractmethod  # Добавляем импорт ABC и abstractmethod

class Approximator(ABC):
    """Abstract base class for function approximators."""
    @abstractmethod
    def compute(self, x):
        """Compute the approximation for a given x.

        Args:
            x (float): Input value.

        Returns:
            float: Approximated value.
        """
        pass

class FunctionApproximator(Approximator):
    """Class to approximate arccos(x) using Taylor series.

    Attributes:
        x_values (np.ndarray): X values.
        n (int): Number of terms.
        approximations (list): Approximated values.
    """
    def __init__(self, x_start, x_end, num_points, n_terms):
        """Initialize approximator.

        Args:
            x_start (float): Start value.
            x_end (float): End value.
            num_points (int): Number of points.
            n_terms (int): Terms in series.
        """
        super().__init__()
        self.x_values = np.linspace(x_start, x_end, num_points)
        self.n = n_terms
        self.approximations = [self.compute(x) for x in self.x_values]

    def compute(self, x):
        """Compute arccos(x) series.

        Args:
            x (float): Value to compute.

        Returns:
            float: Approximated value.

        Raises:
            ValueError: If x is not in [-1, 1].
        """
        if not -1 <= x <= 1:
            raise ValueError("x must be in [-1, 1]")
        result = math.pi / 2
        for k in range(self.n):
            term = math.factorial(2*k) / (4**k * math.factorial(k)**2 * (2*k + 1)) * x**(2*k + 1)
            result -= term
        return result

    def __str__(self):
        """String representation.

        Returns:
            str: String representation.
        """
        return f"FunctionApproximator with {self.n} terms over {len(self.x_values)} points"