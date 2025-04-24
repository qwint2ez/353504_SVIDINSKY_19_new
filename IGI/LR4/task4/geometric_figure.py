"""
GeometricFigure abstract base class for Task 4.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24

This module defines the abstract base class for geometric figures.
"""
from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""
    @abstractmethod
    def area(self):
        """Calculate the area of the geometric figure.

        Returns:
            float: The area of the figure.
        """
        pass

    @abstractmethod
    def display_info(self):
        """Display information about the figure.

        Returns:
            str: A string containing information about the figure.
        """
        pass