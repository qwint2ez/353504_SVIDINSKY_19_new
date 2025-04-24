"""
Main module for Task 2: Text analysis.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24

This module provides the main function to run Task 2, analyzing text from a file or user input.
"""
from task2.text_analyzer import TextAnalyzer

def run_task2():
    """Run Task 2 by reading text from a file or user input, analyzing it, and saving results."""
    print("=== Task 2: Text Analysis ===")
    input_file = "input.txt"
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