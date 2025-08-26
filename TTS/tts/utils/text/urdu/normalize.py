# File: /TTS/tts/utils/text/urdu/normalize.py

import re
from typing import List, Dict

# Urdu-specific normalization patterns
URDU_NUMBER_MAP = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
}

# Common Urdu abbreviations and their expansions
URDU_ABBREVIATIONS = {
    'ڈاکٹر': 'ڈاکٹر',
    'پروفیسر': 'پروفیسر',
    'جناب': 'جناب',
    'محترم': 'محترم',
    'صاحب': 'صاحب',
    'بیگم': 'بیگم',
    'مسٹر': 'مسٹر',
    'مس': 'مس',
}

def normalize_numbers(text: str) -> str:
    """Convert Urdu-Indic numerals to Arabic numerals"""
    for urdu_num, arabic_num in URDU_NUMBER_MAP.items():
        text = text.replace(urdu_num, arabic_num)
    return text

def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in Urdu text"""
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def normalize_punctuation(text: str) -> str:
    """Normalize Urdu punctuation"""
    # Replace multiple punctuation with single
    text = re.sub(r'[۔]{2,}', '۔', text)  # Multiple full stops
    text = re.sub(r'[؟]{2,}', '؟', text)  # Multiple question marks
    text = re.sub(r'[!]{2,}', '!', text)   # Multiple exclamations
    
    # Add space after punctuation if missing
    text = re.sub(r'([۔؟!،])([^\s۔؟!،])', r'\1 \2', text)
    
    return text

def normalize_diacritics(text: str, remove_diacritics: bool = False) -> str:
    """Handle Urdu diacritics"""
    if remove_diacritics:
        # Remove common diacritics for simplified processing
        diacritics = ['َ', 'ِ', 'ُ', 'ً', 'ٍ', 'ٌ', 'ْ', 'ّ']
        for diacritic in diacritics:
            text = text.replace(diacritic, '')
    return text

def normalize_character_variants(text: str) -> str:
    """Normalize character variants in Urdu"""
    # Normalize different forms of the same character
    replacements = {
        'ك': 'ک',  # Arabic kaf to Urdu kaf
        'ي': 'ی',  # Arabic yeh to Urdu yeh
        'ء': 'ٔ',  # Hamza variants
        'أ': 'ا',  # Alif with hamza above
        'إ': 'ا',  # Alif with hamza below
        'آ': 'آ',  # Alif with madda (keep as is)
    }
    
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    
    return text

def expand_abbreviations(text: str) -> str:
    """Expand common Urdu abbreviations"""
    words = text.split()
    expanded_words = []
    
    for word in words:
        # Remove punctuation for matching
        clean_word = re.sub(r'[۔؟!،]', '', word)
        if clean_word in URDU_ABBREVIATIONS:
            # Keep original punctuation
            punctuation = re.findall(r'[۔؟!،]', word)
            expanded = URDU_ABBREVIATIONS[clean_word]
            if punctuation:
                expanded += punctuation[0]
            expanded_words.append(expanded)
        else:
            expanded_words.append(word)
    
    return ' '.join(expanded_words)

def normalize_urdu_text(text: str, 
                       remove_diacritics: bool = False,
                       expand_abbrev: bool = True) -> str:
    """
    Complete Urdu text normalization pipeline
    
    Args:
        text: Input Urdu text
        remove_diacritics: Whether to remove diacritics
        expand_abbrev: Whether to expand abbreviations
    
    Returns:
        Normalized Urdu text
    """
    if not text:
        return text
    
    # Step 1: Normalize character variants
    text = normalize_character_variants(text)
    
    # Step 2: Normalize numbers
    text = normalize_numbers(text)
    
    # Step 3: Handle diacritics
    text = normalize_diacritics(text, remove_diacritics)
    
    # Step 4: Normalize punctuation
    text = normalize_punctuation(text)
    
    # Step 5: Expand abbreviations if requested
    if expand_abbrev:
        text = expand_abbreviations(text)
    
    # Step 6: Normalize whitespace (final step)
    text = normalize_whitespace(text)
    
    return text

def preprocess_for_tts(text: str) -> str:
    """
    Preprocess Urdu text specifically for TTS
    This is optimized for speech synthesis
    """
    # More aggressive normalization for TTS
    text = normalize_urdu_text(
        text, 
        remove_diacritics=True,  # Usually better for TTS
        expand_abbrev=True
    )
    
    # Additional TTS-specific preprocessing
    # Convert numbers to words (you'd need a proper number-to-words implementation)
    # For now, we'll keep numbers as digits
    
    # Ensure sentences end properly
    if text and not text[-1] in '۔؟!':
        text += '۔'
    
    return text

# Example usage and testing
if __name__ == "__main__":
    test_texts = [
        "یہ   ایک    ٹیسٹ ہے۔۔۔",
        "سلام علیکم! آپ کیسے ہیں؟؟",
        "۱۲۳ نمبر گھر میں ڈاکٹر صاحب رہتے ہیں۔",
        "اس میں بہت سارے    اضافی اسپیسز ہیں۔"
    ]
    
    for text in test_texts:
        normalized = normalize_urdu_text(text)
        tts_ready = preprocess_for_tts(text)
        print(f"Original: {text}")
        print(f"Normalized: {normalized}")
        print(f"TTS Ready: {tts_ready}")
        print("-" * 50)
