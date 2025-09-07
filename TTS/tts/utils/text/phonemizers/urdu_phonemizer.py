# File: /TTS/tts/utils/text/phonemizers/urdu_phonemizer.py
from typing import Dict
from TTS.tts.utils.text.urdu.phonemizer import urdu_text_to_phonemes, normalize_urdu_text, add_custom_phoneme
from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_UR_PUNCS = "۔؍،؞؎؏؋٭٪٬٫"  # Urdu punctuation marks

class UrduPhonemizer(BasePhonemizer):
    """🐸TTS Urdu phonemizer with AUTOMATIC three-tier fallback system
    
    AUTOMATIC PROCESS (no configuration needed):
    1. CUSTOM DICTIONARY: Built-in phonemes for problematic words
    2. ESPEAK-NG: For unknown words using Urdu voice
    3. RULE-BASED: Final fallback for any remaining words
    
    Example:
        >>> from TTS.tts.utils.text.phonemizers import UrduPhonemizer
        >>> phonemizer = UrduPhonemizer()
        >>> phonemizer.phonemize("السلام علیکم", separator="|")
        'ɑ|s|ː|ɑ|l|ɑ|ː|m| |ɑ|l|ɑ|ɪ|k|u|m'
    """
    
    language = "ur"
    
    def __init__(self, punctuations=_DEF_UR_PUNCS, keep_puncs=True, use_espeak=True, **kwargs):
        """
        Args:
            punctuations: Urdu punctuation marks to handle
            keep_puncs: Whether to keep punctuation in output
            use_espeak: Whether to use espeak-ng as tier 2 (custom dict is always tier 1)
        """
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)
        self.use_espeak = use_espeak
        print(f"🚀 UrduPhonemizer initialized with automatic three-tier system")
        print(f"   Tier 1: CUSTOM_DICTIONARY (always enabled)")
        print(f"   Tier 2: ESPEAK-NG ({'enabled' if use_espeak else 'disabled'})")
        print(f"   Tier 3: RULE_BASED (always enabled as final fallback)")
    
    @staticmethod
    def name():
        return "urdu_phonemizer"
    
    def add_word_phoneme(self, word: str, phoneme: str):
        """Add a custom word-phoneme mapping to the built-in dictionary"""
        add_custom_phoneme(word, phoneme)
    
    def _phonemize(self, text: str, separator: str = "|") -> str:
        """Convert Urdu text to IPA phonemes using automatic three-tier system"""
        # Normalize text first
        text = normalize_urdu_text(text)
        
        # Get phonemes using AUTOMATIC three-tier system
        print(f"🔄 Processing: {text[:50]}...")
        phonemes = urdu_text_to_phonemes(text, use_espeak=self.use_espeak)
        print(f"✅ Result: {phonemes[:50]}...")
        
        # Apply separator if specified
        if separator and separator != "":
            # Split phonemes and join with separator
            phoneme_chars = list(phonemes.replace(' ', f' {separator} '))
            return separator.join(phoneme_chars)
        
        return phonemes
    
    def phonemize(self, text: str, separator: str = "|", language=None) -> str:
        """Public phonemization method - AUTOMATIC processing"""
        return self._phonemize(text, separator)
    
    @staticmethod
    def supported_languages() -> Dict:
        return {"ur": "urdu"}
    
    def version(self) -> str:
        return "2.0.0-auto"  # Auto three-tier system
    
    def is_available(self) -> bool:
        """Check if the phonemizer is available - Always True (has rule-based fallback)"""
        return True
    
    @classmethod
    def is_supported_language(cls, language):
        """Check if language is supported"""
        return language.lower() in ["ur", "urdu"]

# Test section (only runs when file is executed directly)
if __name__ == "__main__":
    # Test the AUTOMATIC three-tier phonemizer
    phonemizer = UrduPhonemizer()
    
    test_texts = [
        "السلام علیکم",
        "assalam u alaikum", 
        "pakistan zindabad",
        "یہ ایک ٹیسٹ ہے۔"
    ]
    
    print(f"Supported languages: {phonemizer.supported_languages()}")
    print(f"Version: {phonemizer.version()}")
    print(f"Is available: {phonemizer.is_available()}")
    
    for text in test_texts:
        result = phonemizer.phonemize(text, separator="|")
        print(f"'{text}' -> '{result}'")
