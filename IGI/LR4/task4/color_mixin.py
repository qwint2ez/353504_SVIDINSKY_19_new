"""
ColorMixin for Task 4.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module provides a mixin class to add color functionality to geometric figures.
"""

class ColorMixin:
    """Mixin class to add color property to geometric figures."""
    def __init__(self):
        """Initialize the mixin with a default color."""
        self._color = "black"  # Default color

    @property
    def color(self):
        """Get the color of the figure.

        Returns:
            str: The color of the figure.
        """
        return self._color

    @color.setter
    def color(self, value):
        """Set the color of the figure.

        Args:
            value (str): The new color.

        Raises:
            ValueError: If the color is not a string.
        """
        if not isinstance(value, str):
            raise ValueError("Color must be a string")
        self._color = value