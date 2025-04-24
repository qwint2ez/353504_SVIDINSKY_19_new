"""
TextAnalyzer class for Task 2: Text analysis using regex.
Lab Work #4, Version 1.0, Developer: John Doe, Date: 2025-04-24

This module defines the TextAnalyzer class for analyzing text according to the task requirements.
"""
import re
import zipfile

class FileHandlerMixin:
    """Mixin to handle file operations."""
    def save_results(self, filename, results):
        """Save analysis results to a file.

        Args:
            filename (str): Output file.
            results (dict): Results to save.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for k, v in results.items():
                f.write(f"{k}: {v}\n")

    def archive_results(self, input_file, archive_file):
        """Archive the results file using zipfile.

        Args:
            input_file (str): File to archive.
            archive_file (str): Archive file name.

        Returns:
            str: Information about the archived file.
        """
        with zipfile.ZipFile(archive_file, 'w') as zf:
            zf.write(input_file)
        with zipfile.ZipFile(archive_file, 'r') as zf:
            info = zf.getinfo(input_file)
            return f"File size in archive: {info.file_size} bytes"

class TextAnalyzer(FileHandlerMixin):
    """Class to analyze text.

    Attributes:
        text (str): Text to analyze.
    """
    def __init__(self, text):
        """Initialize with text.

        Args:
            text (str): Input text.
        """
        super().__init__()  # Initialize mixin
        self.text = text

    def analyze(self):
        """Analyze the text and return results according to task requirements.

        Returns:
            dict: Analysis results.
        """
        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', self.text.strip())
        results = {
            'total_sentences': len(sentences),
            'narrative': len([s for s in sentences if s.endswith('.')]),
            'interrogative': len([s for s in sentences if s.endswith('?')]),
            'imperative': len([s for s in sentences if s.endswith('!')])
        }

        # Average sentence length (only words)
        words_per_sentence = [re.findall(r'\b\w+\b', s) for s in sentences]
        sentence_lengths = [sum(len(word) for word in words) for words in words_per_sentence]
        results['avg_sentence_len'] = sum(sentence_lengths) / len(sentences) if sentences else 0

        # Average word length
        all_words = re.findall(r'\b\w+\b', self.text)
        results['avg_word_len'] = sum(len(w) for w in all_words) / len(all_words) if all_words else 0

        # Smiley detection
        smiley_pattern = r'[;:]-*((\(+|\)+|\[+|\]+))'
        smileys = re.findall(smiley_pattern, self.text)
        results['smiley_count'] = len([s for s in smileys if len(set(s[0])) == 1])

        # Sentences with spaces, digits, and punctuation
        results['sentences_with_digits'] = [s for s in sentences if re.search(r'\d', s)]

        # Date pattern for dd/mm/yyyy (1600-9999)
        results['date_pattern'] = r'(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/(1[6-9]\d{2}|[2-9]\d{3})'

        # Count uppercase and lowercase letters
        results['uppercase_count'] = len(re.findall(r'[А-ЯA-Z]', self.text))
        results['lowercase_count'] = len(re.findall(r'[а-яa-z]', self.text))

        # Find first word with 'z' and its position
        z_match = re.search(r'\b\w*z\w*\b', self.text, re.IGNORECASE)
        results['z_word'] = z_match.group() if z_match else "Not found"
        results['z_position'] = z_match.start() if z_match else -1

        # Exclude words starting with 'a' or 'A'
        results['no_a_text'] = ' '.join(re.findall(r'\b(?![aAаА])\w+\b', self.text))

        return results

    def __str__(self):
        """String representation of the analyzer.

        Returns:
            str: String representation.
        """
        return f"TextAnalyzer with text of length {len(self.text)}"