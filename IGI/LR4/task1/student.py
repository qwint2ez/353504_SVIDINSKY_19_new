"""
Student class for Task 1, inheriting from Person.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24
"""
from task1.person import Person

class Student(Person):
    """Derived class for student data.

    Uses super() to inherit from Person.
    """
    default_role = "Student"  # Static attribute, overriding parent

    def __init__(self, surname, initials, day, month, year):
        """Initialize a Student instance.

        Args:
            surname (str): Surname.
            initials (str): Initials.
            day (int): Day of birth.
            month (int): Month of birth.
            year (int): Year of birth.
        """
        super().__init__(surname, initials, day, month, year)  # Using super()