# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

from series_calculator import compute_arccos_series, display_results, sum_sequence_last_digits
from utils import get_float_input, repeat_execution
from sequence_utils import initialize_with_input, initialize_with_generator, process_list
from text_analyzer import analyze_text, analyze_string

@repeat_execution
def run_task1():
    """Run Task 1: Compute arccos(x) using series expansion."""
    print("\nTask 1: Compute arccos(x)")
    x = get_float_input("Enter x (-1 to 1): ")
    eps = get_float_input("Enter precision (eps, e.g., 0.0001): ")
    try:
        result, n, math_result = compute_arccos_series(x, eps)
        display_results(x, result, n, math_result, eps)
    except ValueError as e:
        print(f"Error: {e}")

@repeat_execution
def run_task2():
    """Run Task 2: Sum of last digits of numbers until 0 is entered."""
    print("\nTask 2: Sum of last digits")
    result = sum_sequence_last_digits()
    print(f"Sum of last digits: {result}")

@repeat_execution
def run_task3():
    """Run Task 3: Text analysis."""
    print("\nTask 3: Text analysis")
    spaces, digits, punct = analyze_text()
    print(f"Spaces: {spaces}, Digits: {digits}, Punctuation: {punct}")

@repeat_execution
def run_task4():
    """Run Task 4: String analysis."""
    print("\nTask 4: String analysis")
    vowels, freq, after_commas = analyze_string()
    print(f"Words starting/ending with vowels: {vowels}")
    print("Character frequency:", freq)
    print("Words after commas:", after_commas)

@repeat_execution
def run_task5():
    """Run Task 5: List processing."""
    print("\nTask 5: List processing")
    while True:
        size = int(get_float_input("Enter list size (positive number): "))
        if size <= 0:
            print("Size must be a positive number!")
            continue
        break
    print("Choose initialization method:")
    print("1. Manual input")
    print("2. Random generator")
    method = input("Enter 1 or 2: ")
    if method == '1':
        seq = initialize_with_input(size)
    elif method == '2':
        seq = list(initialize_with_generator(size))  # Convert generator to list
    else:
        print("Invalid choice, using manual input by default.")
        seq = initialize_with_input(size)
    max_idx, prod = process_list(seq)
    print(f"List: {seq}")
    print(f"Max element index: {max_idx}, Product of first two non-zeros: {prod}")

def main():
    """Main function to run the program."""
    print("Welcome to Lab Work #3!")
    while True:
        print("\nOptions:")
        print("1. Run Task 1 (arccos(x) series)")
        print("2. Run Task 2 (Sum of last digits)")
        print("3. Run Task 3 (Text analysis)")
        print("4. Run Task 4 (String analysis)")
        print("5. Run Task 5 (List processing)")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")
        if choice == '1':
            run_task1()
        elif choice == '2':
            run_task2()
        elif choice == '3':
            run_task3()
        elif choice == '4':
            run_task4()
        elif choice == '5':
            run_task5()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()