"""
ClassRoom class for Task 1 to manage students.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24
"""
import csv
import pickle
import random
import string
from task1.student import Student  # Добавляем импорт Student

class ClassRoom:
    """Class to manage a collection of students.

    Attributes:
        students (list): List of Student objects.
    """
    def __init__(self):
        """Initialize an empty classroom."""
        self.students = []

    def add_student(self, student):
        """Add a student to the classroom.

        Args:
            student (Student): Student to add.
        """
        self.students.append(student)

    def calculate_average_birthday(self):
        """Calculate the average birthday of students.

        Returns:
            str: Average birthday in dd/mm/yyyy format.

        Raises:
            ValueError: If no students exist.
        """
        if not self.students:
            raise ValueError("No students in the classroom")
        avg_day = round(sum(s._day for s in self.students) / len(self.students))
        avg_month = round(sum(s._month for s in self.students) / len(self.students))
        avg_year = round(sum(s._year for s in self.students) / len(self.students))
        while avg_day > 31:
            avg_day -= 30
            avg_month += 1
        while avg_month > 12:
            avg_month -= 12
            avg_year += 1
        return f"{avg_day:02d}/{avg_month:02d}/{avg_year}"

    def search_student(self, surname):
        """Search students by surname.

        Args:
            surname (str): Surname to search.

        Returns:
            list: List of matching students as strings.
        """
        return [str(s) for s in self.students if s.surname == surname]

    def to_csv(self, filename):
        """Save students to a CSV file.

        Args:
            filename (str): File to save to.
        """
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Surname', 'Initials', 'Day', 'Month', 'Year'])
            for s in self.students:
                writer.writerow([s.surname, s._initials, s._day, s._month, s._year])

    def to_pickle(self, filename):
        """Serialize the classroom to a pickle file.

        Args:
            filename (str): File to save to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def from_pickle(filename):
        """Deserialize a classroom from a pickle file.

        Args:
            filename (str): File to read from.

        Returns:
            ClassRoom: The deserialized classroom.
        """
        with open(filename, 'rb') as f:
            return pickle.load(f)

def generate_random_student():
    """Generate a random student.

    Returns:
        Student: A randomly generated student.
    """
    surname = ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.ascii_lowercase, k=5))
    initials = random.choice(string.ascii_uppercase) + '.' + random.choice(string.ascii_uppercase) + '.'
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1990, 2010)
    return Student(surname, initials, day, month, year)