# File: /TTS/tts/utils/text/urdu/phonemizer.py (Enhanced Version)

import subprocess
import re
from typing import Optional
from .normalize import normalize_urdu_text, preprocess_for_tts

def urdu_text_to_phonemes(text: str, use_espeak: bool = True) -> str:
    """
    Convert Urdu text to IPA phonemes using espeak-ng with enhanced fallback
    
    Args:
        text: Input Urdu text
        use_espeak: Use espeak-ng for phonemization
    
    Returns:
        IPA phonemes string
    """
    # Preprocess text first
    text = preprocess_for_tts(text)
    
    if use_espeak:
        phonemes = _urdu_espeak_phonemize(text)
        # If espeak gives reasonable output, use it; otherwise fallback
        if phonemes and len(phonemes) > 0 and not phonemes.isspace():
            return phonemes
    
    # Fallback to enhanced rule-based approach
    return _urdu_rule_based_phonemize(text)

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
        

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
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

# Keep the original normalize function for backward compatibility
def normalize_urdu_text(text: str) -> str:
    """Normalize Urdu text for better phonemization"""
    # Use the enhanced normalize function
    from .normalize import normalize_urdu_text as enhanced_normalize
    return enhanced_normalize(text)
