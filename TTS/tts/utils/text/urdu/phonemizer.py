# File: /TTS/tts/utils/text/urdu/phonemizer.py (Enhanced Version with Custom Dictionary)

import subprocess
import re
from typing import Optional, Dict
from .normalize import normalize_urdu_text, preprocess_for_tts

# Custom phoneme dictionary for problematic words
CUSTOM_PHONEME_DICT = {
    # Islamic greetings and common phrases
    "السلام علیکم": "æs.sæ.læː.m ʊ a.lɛɪ.kʊm",
    "السلام": "əs.sɑː.ləmU",
    "علیکم": "a.lɛɪ.kʊm",
    #"وعلیکم": "/wa ʕa.laj.kum/",
    "سروس": "sərvɪs",
    "لطف": "lʊt̪f",
    "ہنسی": "/hɛ̃ː.siː/",
    "لین": "leːn",
    "دین": " deːn",
    "کھلاڑی": "kʰɪ.lɑː.ɽiː",
    "سنوارتے": "sə̃.wɑːr.t̪eː",
    "اسکول": "ɪs.kuːl",
    "خوش": "xʊʃ",
    "کسٹمر": "kəs.tə.mər",
    "فراہم": "fə.rɑː.həm",
    "کھلاڑیوں": "kʰɪ.lɑː.ɽi.jõː",
    "میٹنگ": "miː.ʈɪŋ",
    
    # Add more problematic words as you discover them
    # "word": "phoneme",
}

def add_custom_phoneme(word: str, phoneme: str):
    """Add a new word-phoneme mapping to the custom dictionary"""
    CUSTOM_PHONEME_DICT[word.lower()] = phoneme
    
def load_custom_phonemes_from_file(file_path: str):
    """Load custom phonemes from a file (word|phoneme format)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    word, phoneme = line.split('|', 1)
                    CUSTOM_PHONEME_DICT[word.lower().strip()] = phoneme.strip()
    except FileNotFoundError:
        print(f"Custom phoneme file not found: {file_path}")

def urdu_text_to_phonemes(text: str, use_espeak: bool = True, use_custom_dict: bool = True) -> str:
    """
    Convert Urdu text to IPA phonemes with custom dictionary fallback
    
    Args:
        text: Input Urdu text
        use_espeak: Use espeak-ng for phonemization
        use_custom_dict: Use custom dictionary for known problematic words
    
    Returns:
        IPA phonemes string
    """
    # Preprocess text first
    text = preprocess_for_tts(text)
    # Split text into words for individual processing
    words = text.split()
    phoneme_results = []
    
    for word in words:
        # Clean the word (remove punctuation for lookup)
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        
        word_phoneme = ""
        
        # Step 1: Check custom dictionary first
        if clean_word in CUSTOM_PHONEME_DICT:
            word_phoneme = CUSTOM_PHONEME_DICT[clean_word]
            print(f"Custom dict used for '{clean_word}': {word_phoneme}")
        
        # Step 2: If not in custom dict, try espeak
        elif use_espeak:
            word_phoneme = _urdu_espeak_phonemize(word)
            if word_phoneme and len(word_phoneme.strip()) > 0:
                print(f"Espeak used for '{word}': {word_phoneme}")
            else:
                # Step 3: Fallback to rule-based if espeak fails
                word_phoneme = _urdu_rule_based_phonemize(word)
                print(f"Rule-based used for '{word}': {word_phoneme}")
        
        # Step 3: Direct fallback to rule-based if espeak disabled
        else:
            word_phoneme = _urdu_rule_based_phonemize(word)
            print(f"Rule-based used for '{word}': {word_phoneme}")
        
        # Add the result
        if word_phoneme:
            phoneme_results.append(word_phoneme)
    
    # Join all phonemes
    final_phonemes = ' '.join(phoneme_results)
    
    # Final cleanup
    final_phonemes = re.sub(r'\s+', ' ', final_phonemes).strip()
    
    return final_phonemes

def _urdu_espeak_phonemize(text: str) -> str:
    """Use espeak-ng for Urdu phonemization with better error handling"""
    try:
        # Try with Urdu voice first
        cmd = ["espeak-ng", "-q", "-v", "ur", "--ipa", text]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            phonemes = result.stdout.strip()
            # Clean espeak output
            phonemes = re.sub(r'\s+', ' ', phonemes)
            phonemes = re.sub(r'[()]+', '', phonemes)
            return phonemes.strip()
        
        # Try with Hindi voice as fallback (similar phonetics)
        cmd = ["espeak-ng", "-q", "-v", "hi", "--ipa", text]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            phonemes = result.stdout.strip()
            phonemes = re.sub(r'\s+', ' ', phonemes)
            phonemes = re.sub(r'[()]+', '', phonemes)
            return phonemes.strip()

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Espeak failed for '{text}': {e}")
    
    # Return empty string to trigger rule-based fallback
    return ""

def _urdu_rule_based_phonemize(text: str) -> str:
    """
    Enhanced rule-based Urdu to IPA conversion
    Based on Urdu phonology and improved mapping
    """
    
    # Enhanced Urdu to IPA mapping
    urdu_to_ipa = {
        # Vowels (long and short)
        'ا': 'ɑ',      # alif
        'آ': 'ɑː',     # alif madda
        'ای': 'eː',    # yeh with alif
        'او': 'oː',    # waw with alif
        'اے': 'eː',    # alif with yeh
        'اؤ': 'əʊ',    # alif with waw
        'ے': 'eː',     # yeh (final form)
        'ی': 'iː',     # yeh
        'و': 'uː',     # waw (when vowel)
        
        # Short vowels (diacritics)
        'َ': 'a',      # zabar (fatha)
        'ِ': 'i',      # zer (kasra)
        'ُ': 'u',      # pesh (damma)
        'ً': 'aⁿ',     # double zabar (tanween)
        'ٍ': 'iⁿ',     # double zer
        'ٌ': 'uⁿ',     # double pesh
        'ْ': '',       # jazm (sukun) - no vowel
        'ّ': '',       # shaddah (gemination marker)
        
        # Consonants - Stops
        'ب': 'b',      # beh
        'پ': 'p',      # peh
        'ت': 't̪',     # teh (dental)
        'ٹ': 'ʈ',      # tteh (retroflex)
        'ث': 's',      # theh (often pronounced as 's')
        'ج': 'd͡ʒ',     # jeem
        'چ': 't͡ʃ',     # cheh
        'د': 'd̪',     # dal (dental)
        'ڈ': 'ɖ',      # ddal (retroflex)
        'ذ': 'z',      # zal (often pronounced as 'z')
        'ک': 'k',      # kaf
        'گ': 'ɡ',      # gaf
        'ق': 'q',      # qaf (often k in modern Urdu)
        
        # Fricatives
        'ف': 'f',      # feh
        'ث': 's',      # theh
        'س': 's',      # seen
        'ص': 's',      # sad (often 's' in modern Urdu)
        'ش': 'ʃ',      # sheen
        'خ': 'x',      # kheh
        'غ': 'ɣ',      # ghain
        'ح': 'ɦ',      # heh (aspirated)
        'ہ': 'ɦ',      # heh goal
        'ھ': 'ʰ',      # heh doachashmee (aspiration marker)
        'ع': 'ʔ',      # ain (glottal stop in formal speech)
        'ز': 'z',      # zain
        'ژ': 'ʒ',      # zheh
        'ض': 'z',      # dad (often 'z' in modern Urdu)
        'ط': 't̪',     # tah (often dental 't')
        'ظ': 'z',      # zah (often 'z')
        
        # Nasals
        'م': 'm',      # meem
        'ن': 'n',      # noon
        'ں': 'ɰ̃',     # noon ghunna (nasalization)
        
        # Liquids
        'ل': 'l',      # lam
        'ر': 'r',      # reh (usually trilled)
        'ڑ': 'ɽ',      # rreh (retroflex flap)
        
        # Semi-vowels/Glides
        'و': 'ʋ',      # waw (when consonant)
        'ی': 'j',      # yeh (when consonant)
        
        # Numbers (Arabic-Indic to phonetic)
        '۰': 'sɪfr',   # 0
        '۱': 'ek',     # 1  
        '۲': 'd̪oː',    # 2
        '۳': 't̪iːn',   # 3
        '۴': 't͡ʃaːr',  # 4
        '۵': 'paːnt͡ʃ', # 5
        '۶': 't͡ʃʰeː',  # 6
        '۷': 'saːt̪',   # 7
        '۸': 'aːʈʰ',   # 8
        '۹': 'nəʊ',    # 9
        
        # Common punctuation
        '۔': '.',      # Urdu full stop
        '؟': '?',      # Urdu question mark
        '،': ',',      # Urdu comma
    }
    
    result = []
    i = 0
    
    while i < len(text):
        # Check for two-character combinations first
        if i < len(text) - 1:
            two_char = text[i:i+2]
            if two_char in urdu_to_ipa:
                result.append(urdu_to_ipa[two_char])
                i += 2
                continue
        
        # Single character mapping
        char = text[i]
        if char in urdu_to_ipa:
            phoneme = urdu_to_ipa[char]
            if phoneme:  # Skip empty phonemes (like jazm)
                result.append(phoneme)
        elif char.isspace():
            result.append(' ')
        elif char.isascii():
            # Keep ASCII characters as-is (for mixed text)
            result.append(char)
        # Skip unknown characters
        
        i += 1
    
    # Post-processing
    phonemes = ''.join(result)
    
    # Handle common phonetic combinations and rules
    phonemes = _apply_urdu_phonetic_rules(phonemes)
    
    return phonemes

def _apply_urdu_phonetic_rules(phonemes: str) -> str:
    """Apply Urdu-specific phonetic rules"""
    
    # Rule 1: Vowel harmony and length
    # Simplify repeated vowels
    phonemes = re.sub(r'([aiu])\1+', r'\1', phonemes)
    
    # Rule 2: Consonant clusters
    # Simplify some difficult consonant clusters
    phonemes = re.sub(r'([kɡq])([ʰ])', r'\1ʰ', phonemes)  # Aspiration
    
    # Rule 3: Word boundaries
    # Ensure proper spacing
    phonemes = re.sub(r'\s+', ' ', phonemes)
    
    # Rule 4: Final cleanup
    phonemes = phonemes.strip()
    
    return phonemes

# Utility functions for managing custom dictionary
def export_custom_dict_to_file(file_path: str):
    """Export current custom dictionary to a file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for word, phoneme in sorted(CUSTOM_PHONEME_DICT.items()):
            f.write(f"{word}|{phoneme}\n")

def get_phonemization_stats(text: str):
    """Get statistics on which method was used for each word"""
    words = text.split()
    stats = {"custom": 0, "espeak": 0, "rule_based": 0}
    
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        
        if clean_word in CUSTOM_PHONEME_DICT:
            stats["custom"] += 1
        else:
            espeak_result = _urdu_espeak_phonemize(word)
            if espeak_result and len(espeak_result.strip()) > 0:
                stats["espeak"] += 1
            else:
                stats["rule_based"] += 1
    
    return stats

# Keep the original normalize function for backward compatibility
def normalize_urdu_text(text: str) -> str:
    """Normalize Urdu text for better phonemization"""
    # Use the enhanced normalize function
    from .normalize import normalize_urdu_text as enhanced_normalize
    return enhanced_normalize(text)

# Example usage and testing
if __name__ == "__main__":
    # Test the phonemizer
    test_texts = [
        "السلام علیکم",           # Urdu script - will use CUSTOM_DICT
        "assalam u alaikum",      # Roman - will use CUSTOM_DICT  
        "bismillah hir rahman",   # Mixed - will use CUSTOM_DICT + others
        "pakistan zindabad",      # Mixed - will use CUSTOM_DICT + others
        "یہ ایک ٹیسٹ ہے"          # Pure Urdu - will use RULE_BASED
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        phonemes = urdu_text_to_phonemes(text)
        print(f"Phonemes: {phonemes}")
        stats = get_phonemization_stats(text)
        print(f"Stats: {stats}")
