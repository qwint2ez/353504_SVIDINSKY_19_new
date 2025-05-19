"""
Main module for Task 2: Text analysis.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module provides the main function to run Task 2, analyzing text from a file or user input.
"""
import os
from task2.text_analyzer import TextAnalyzer

def run_task2():
    """Run Task 2 by reading text from a file or user input, analyzing it, and saving results."""
    print("=== Task 2: Text Analysis ===")
    input_file = "task2/input.txt"
    output_file = "results.txt"
    archive_file = "results.zip"

    # Спрашиваем пользователя, как он хочет ввести текст
    choice = input("Do you want to (1) read text from a file or (2) input text manually? (1/2): ")
    
    if choice == '2':
        text = input("Enter the text to analyze: ")
        print("Text entered manually.")
    else:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"Text loaded from {input_file}")
        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found.")
            create_file = input("Would you like to create the file and input text? (y/n): ").lower()
            if create_file == 'y':
                text = input("Enter the text to save in the file: ")
                try:
                    # Убедимся, что директория существует
                    os.makedirs(os.path.dirname(input_file), exist_ok=True)
                    with open(input_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"File '{input_file}' created successfully.")
                except Exception as e:
                    print(f"Error creating file: {e}")
                    print("Switching to manual input.")
                    text = input("Enter the text to analyze: ")
            else:
                print("Switching to manual input.")
                text = input("Enter the text to analyze: ")
        except Exception as e:
            print(f"Error: {e}")
            print("Switching to manual input.")
            text = input("Enter the text to analyze: ")

    try:
        # Analyze text
        analyzer = TextAnalyzer(text)
        results = analyzer.analyze()

        # Print results to screen
        print("\nAnalysis Results:")
        for key, value in results.items():
            print(f"{key}: {value}")

        # Save results to file
        analyzer.save_results(output_file, results)
        print(f"\nResults saved to {output_file}")

        # Archive results
        archive_info = analyzer.archive_results(output_file, archive_file)
        print(f"Results archived to {archive_file}")
        print(archive_info)

    except Exception as e:
        print(f"Error during analysis or archiving: {e}")

if __name__ == "__main__":
    run_task2()