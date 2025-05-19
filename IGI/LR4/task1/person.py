"""
Person base class for Task 1.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24
"""

class Person:
    """Base class for person data with static and dynamic attributes.

    Attributes:
        _surname (str): Surname of the person.
        _initials (str): Initials of the person.
        _day (int): Day of birth.
        _month (int): Month of birth.
        _year (int): Year of birth.
    """
    default_role = "Person"  # Static attribute

    def __init__(self, surname, initials, day, month, year):
        """Initialize a Person instance.

        Args:
            surname (str): Surname.
            initials (str): Initials.
            day (int): Day of birth.
            month (int): Month of birth.
            year (int): Year of birth.
        """
        self._surname = surname
        self._initials = initials
        self._day = day
        self._month = month
        self._year = year

    @property
    def surname(self):
        """Get surname."""
        return self._surname

    @surname.setter
    def surname(self, value):
        """Set surname."""
        if not isinstance(value, str):
            raise ValueError("Surname must be a string")
        self._surname = value

    def __str__(self):
        """String representation of the person."""
        return f"{self._surname} {self._initials}, {self._day:02d}/{self._month:02d}/{self._year}"

    def __eq__(self, other):
        """Compare two persons by birth date."""
        if not isinstance(other, Person):
            return False
        return (self._day, self._month, self._year) == (other._day, other._month, other._year)