# Lab Work #3: Standard Data Types, Collections, Functions, Modules
# Version: 1.0
# Developer: Alexander Svidinsky
# Date: 09.04.2024

def analyze_text():
    """
    Count spaces, digits, and punctuation in a text.

    Returns:
        tuple: (spaces, digits, punctuation)
    """
    text = input("Enter text: ")
    spaces = text.count(" ")
    digits = sum(c.isdigit() for c in text)
    punctuation = sum(c in ".,!?;:" for c in text)
    return spaces, digits, punctuation

def analyze_string():
    """
    Analyze a predefined string for vowels, frequency, and words after commas.

    Returns:
        tuple: (vowel_words, char_freq, words_after_commas)
    """
    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    vowels = "aeiou"
    words = text.replace(",", " ").split()
    
    vowel_words = len([w for w in words if w[0].lower() in vowels or w[-1].lower() in vowels])
    
    char_freq = {}
    for char in text.lower():
        if char.isalpha():
            char_freq[char] = char_freq.get(char, 0) + 1
    
    parts = text.split(",")
    words_after_commas = [part.strip().split()[0] for part in parts[1:]]
    words_after_commas.sort()
    
    return vowel_words, char_freq, words_after_commas