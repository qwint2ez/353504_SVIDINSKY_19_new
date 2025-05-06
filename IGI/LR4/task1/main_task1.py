"""
Main module for Task 1: Manage school class data.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24
"""
from task1.classroom import ClassRoom, generate_random_student
from task1.student import Student  # Добавляем импорт класса Student
from utilities.input_utils import get_valid_int

def run_task1():
    classroom = ClassRoom()
    print("=== Task 1: Manage School Class ===")
    choice = input("Do you want to (1) manually input students or (2) auto-generate? (1/2): ")
    
    if choice == '2':
        num_students = get_valid_int("How many students to generate (1-10)? ", 1, 10)
        for _ in range(num_students):
            classroom.add_student(generate_random_student())
        print(f"Generated {num_students} students.")
    else:
        while True:
            try:
                surname = input("Enter surname: ")
                initials = input("Enter initials (e.g., I.I.): ")
                day = get_valid_int("Enter day (1-31): ", 1, 31)
                month = get_valid_int("Enter month (1-12): ", 1, 12)
                year = get_valid_int("Enter year (1900-2023): ", 1900, 2023)
                student = Student(surname, initials, day, month, year)
                classroom.add_student(student)
                if input("Add another student? (y/n): ").lower() != 'y':
                    break
            except ValueError as e:
                print(f"Error: {e}")

    if classroom.students:
        classroom.to_csv("students.csv")
        classroom.to_pickle("students.pkl")  # Добавляем сохранение в pickle
        print("Data saved to students.csv and students.pkl")
        print("Average birthday:", classroom.calculate_average_birthday())
        search = input("Search student by surname: ")
        results = classroom.search_student(search)
        print("Found students:", results if results else "No students found.")
    else:
        print("No students added.")