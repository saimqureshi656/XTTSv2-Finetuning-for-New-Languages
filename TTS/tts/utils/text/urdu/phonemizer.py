import subprocess
import re
from typing import Optional

def urdu_text_to_phonemes(text: str, use_espeak: bool = True) -> str:
    """
    Convert Urdu text to IPA phonemes using espeak-ng
    
    Args:
        text: Input Urdu text
        use_espeak: Use espeak-ng for phonemization
    
    Returns:
        IPA phonemes string
    """
    if use_espeak:
        return _urdu_espeak_phonemize(text)
    else:
        # Fallback to rule-based approach
        return _urdu_rule_based_phonemize(text)

def _urdu_espeak_phonemize(text: str) -> str:
    """Use espeak-ng for Urdu phonemization"""
    try:
        # Use espeak-ng with Urdu voice
        cmd = ["espeak-ng", "-q", "-v", "ur", "--ipa", text]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            phonemes = result.stdout.strip()
            # Clean espeak output
            phonemes = re.sub(r'\s+', ' ', phonemes)  # Normalize whitespace
            phonemes = re.sub(r'[()]+', '', phonemes)  # Remove parentheses
            return phonemes.strip()
        else:
            # Fallback if espeak fails
            return _urdu_rule_based_phonemize(text)
            
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # Fallback if espeak is not available
        return _urdu_rule_based_phonemize(text)

def _urdu_rule_based_phonemize(text: str) -> str:
    """
    Basic rule-based Urdu to IPA conversion
    This is a simplified version - expand with proper Urdu phonetic rules
    """
    # Basic Urdu to IPA mapping (expand this significantly)
    urdu_to_ipa = {
        # Vowels
        'ا': 'ɑ',
        'آ': 'ɑː',
        'ای': 'eː',
        'او': 'oː',
        'اے': 'eː',
        'اؤ': 'əʊ',
        
        # Common consonants
        'ب': 'b',
        'پ': 'p',
        'ت': 't̪',
        'ٹ': 'ʈ',
        'ث': 's',
        'ج': 'd͡ʒ',
        'چ': 't͡ʃ',
        'ح': 'ɦ',
        'خ': 'x',
        'د': 'd̪',
        'ڈ': 'ɖ',
        'ذ': 'z',
        'ر': 'ɾ',
        'ڑ': 'ɽ',
        'ز': 'z',
        'ژ': 'ʒ',
        'س': 's',
        'ش': 'ʃ',
        'ص': 's',
        'ض': 'z',
        'ط': 't̪',
        'ظ': 'z',
        'ع': 'ʕ',
        'غ': 'ɣ',
        'ف': 'f',
        'ق': 'q',
        'ک': 'k',
        'گ': 'ɡ',
        'ل': 'l',
        'م': 'm',
        'ن': 'n',
        'ں': 'ɰ̃',
        'و': 'ʋ',
        'ہ': 'ɦ',
        'ھ': 'ʰ',
        'ی': 'j',
        'ے': 'eː',
        
        # Diacritics (if present)
        'َ': 'a',  # zabar
        'ِ': 'i',  # zer
        'ُ': 'u',  # pesh
        'ً': 'an', # double zabar
        'ٍ': 'in', # double zer
        'ٌ': 'un', # double pesh
        'ْ': '',   # jazm (no vowel)
        'ّ': '',   # shaddah (gemination - handle specially)
    }
    
    result = []
    for char in text:
        if char in urdu_to_ipa:
            result.append(urdu_to_ipa[char])
        elif char.isspace():
            result.append(' ')
        else:
            # Keep unknown characters as-is or skip
            result.append(char)
    
    return ''.join(result)

def normalize_urdu_text(text: str) -> str:
    """Normalize Urdu text for better phonemization"""
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Normalize some common character variants
    text = text.replace('ک', 'ک')  # Normalize kaf variants
    text = text.replace('ی', 'ی')  # Normalize yeh variants
    
    return text
