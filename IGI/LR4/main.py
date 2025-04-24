"""
Main module to test all tasks.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24
"""
from task1.main_task1 import run_task1
from task2.main_task2 import run_task2
from task3.main_task3 import run_task3
from task4.main_task4 import run_task4
from task5.main_task5 import run_task5

def main():
    """Main function with menu and repeat functionality."""
    tasks = {
        '1': ("Task 1: School Class", run_task1),
        '2': ("Task 2: Text Analysis", run_task2),
        '3': ("Task 3: Function Plotting", run_task3),
        '4': ("Task 4: Geometric Figures", run_task4),
        '5': ("Task 5: Matrix Operations", run_task5)
    }
    while True:
        print("\n=== Lab Work #4 Menu ===")
        for key, (desc, _) in tasks.items():
            print(f"{key}: {desc}")
        choice = input("Select task (1-5) or 'q' to quit: ")
        if choice == 'q':
            break
        if choice in tasks:
            try:
                tasks[choice][1]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice")
        if input("Continue? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()