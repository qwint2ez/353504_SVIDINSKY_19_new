"""
Trapezoid class for Task 4.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module defines the Trapezoid class, which inherits from GeometricFigure and uses ColorMixin.
"""
from task4.geometric_figure import GeometricFigure
from task4.color_mixin import ColorMixin

class Trapezoid(GeometricFigure, ColorMixin):
    """Class representing a Trapezoid, inheriting from GeometricFigure and ColorMixin."""
    name = "Trapezoid"  # Static attribute

    def __init__(self, h, a, b, color):
        """Initialize a Trapezoid.

        Args:
            h (float): Height of the trapezoid.
            a (float): First base of the trapezoid.
            b (float): Middle line of the trapezoid.
            color (str): Color of the trapezoid.
        """
        super().__init__()  # Initialize ColorMixin
        self._h = float(h)
        self._a = float(a)
        self._b = float(b)
        self._c = 2 * self._b - self._a  # Second base, dynamic attribute
        self.color = color  # Using ColorMixin setter

    @property
    def height(self):
        """Get the height of the trapezoid.

        Returns:
            float: The height.
        """
        return self._h

    @height.setter
    def height(self, value):
        """Set the height of the trapezoid.

        Args:
            value (float): The new height.

        Raises:
            ValueError: If height is not positive.
        """
        if value <= 0:
            raise ValueError("Height must be positive")
        self._h = float(value)

    @property
    def base_a(self):
        """Get the first base of the trapezoid.

        Returns:
            float: The first base.
        """
        return self._a

    @base_a.setter
    def base_a(self, value):
        """Set the first base of the trapezoid.

        Args:
            value (float): The new base.

        Raises:
            ValueError: If base is not positive.
        """
        if value <= 0:
            raise ValueError("Base a must be positive")
        self._a = float(value)
        self._c = 2 * self._b - self._a  # Update second base

    @property
    def middle_line(self):
        """Get the middle line of the trapezoid.

        Returns:
            float: The middle line.
        """
        return self._b

    @middle_line.setter
    def middle_line(self, value):
        """Set the middle line of the trapezoid.

        Args:
            value (float): The new middle line.

        Raises:
            ValueError: If middle line is invalid.
        """
        if value <= self._a / 2:
            raise ValueError(f"Middle line must be greater than {self._a / 2}")
        self._b = float(value)
        self._c = 2 * self._b - self._a  # Update second base

    def area(self):
        """Calculate the area of the trapezoid (polymorphism example).

        Returns:
            float: The area.
        """
        return (self._a + self._c) * self._h / 2

    def display_info(self):
        """Display information about the trapezoid (polymorphism example).

        Returns:
            str: Information about the trapezoid.
        """
        return f"{self.name}: h={self._h:.2f}, a={self._a:.2f}, b={self._b:.2f}, color={self.color}, area={self.area():.2f}"

    def __str__(self):
        """String representation of the trapezoid (magic method).

        Returns:
            str: String representation.
        """
        return self.display_info()

    def __eq__(self, other):
        """Compare two trapezoids by area (magic method).

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if areas are equal, False otherwise.
        """
        if not isinstance(other, Trapezoid):
            return False
        return abs(self.area() - other.area()) < 1e-6

    @classmethod
    def get_name(cls):
        """Return the name of the figure (class method).

        Returns:
            str: The name of the figure.
        """
        return cls.name