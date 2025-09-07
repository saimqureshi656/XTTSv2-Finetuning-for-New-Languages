# File: /TTS/tts/utils/text/phonemizers/urdu_phonemizer.py
from typing import Dict
from TTS.tts.utils.text.urdu.phonemizer import urdu_text_to_phonemes, normalize_urdu_text, add_custom_phoneme, load_custom_phonemes_from_file
from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_UR_PUNCS = "۔؍،؞؎؏؋٭٪٬٫"  # Urdu punctuation marks

class UrduPhonemizer(BasePhonemizer):
    """🐸TTS Urdu phonemizer using custom dictionary + espeak-ng + rule-based fallback
    
    This phonemizer converts Urdu text to IPA phonemes using:
    1. Primary: Custom dictionary for problematic words
    2. Secondary: espeak-ng with Urdu voice
    3. Fallback: Rule-based Urdu to IPA conversion
    
    Example:
        >>> from TTS.tts.utils.text.phonemizers import UrduPhonemizer
        >>> phonemizer = UrduPhonemizer()
        >>> phonemizer.phonemize("السلام علیکم", separator="|")
        'ɑ|s|ː|ɑ|l|ɑ|ː|m| |ɑ|l|ɑ|ɪ|k|u|m'
    """
    
    language = "ur"
    
    def __init__(self, punctuations=_DEF_UR_PUNCS, keep_puncs=True, use_espeak=True, 
                 use_custom_dict=True, custom_phoneme_file=None, **kwargs):
        """
        Args:
            punctuations: Urdu punctuation marks to handle
            keep_puncs: Whether to keep punctuation in output
            use_espeak: Whether to use espeak-ng as secondary method
            use_custom_dict: Whether to use custom dictionary as primary method
            custom_phoneme_file: Path to custom phoneme dictionary file
        """
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)
        self.use_espeak = use_espeak
        self.use_custom_dict = use_custom_dict
        
        # Load custom phonemes from file if provided
        if custom_phoneme_file:
            try:
                load_custom_phonemes_from_file(custom_phoneme_file)
                print(f"✅ Loaded custom phonemes from: {custom_phoneme_file}")
            except Exception as e:
                print(f"⚠️ Failed to load custom phonemes: {e}")
    
    @staticmethod
    def name():
        return "urdu_phonemizer"
    
    def add_word_phoneme(self, word: str, phoneme: str):
        """Add a custom word-phoneme mapping"""
        add_custom_phoneme(word, phoneme)
        print(f"✅ Added custom phoneme: '{word}' -> '{phoneme}'")
    
    def _phonemize(self, text: str, separator: str = "|") -> str:
        """Convert Urdu text to IPA phonemes"""
        # Normalize text first
        text = normalize_urdu_text(text)
        
        # Get phonemes using the enhanced three-tier system
        print(f"🔎 UrduPhonemizer is processing: {text[:50]}...")
        phonemes = urdu_text_to_phonemes(
            text, 
            use_espeak=self.use_espeak,
            use_custom_dict=self.use_custom_dict
        )
        print(f"👉 Produced phonemes: {phonemes[:50]}...")
        
        # Apply separator if specified
        if separator and separator != "":
            # Split phonemes and join with separator
            phoneme_chars = list(phonemes.replace(' ', f' {separator} '))
            return separator.join(phoneme_chars)
        
        return phonemes
    
    def phonemize(self, text: str, separator: str = "|", language=None) -> str:
        """Public phonemization method"""
        return self._phonemize(text, separator)
    
    @staticmethod
    def supported_languages() -> Dict:
        return {"ur": "urdu"}
    
    def version(self) -> str:
        return "2.0.0"  # Updated version with custom dictionary support
    
    def is_available(self) -> bool:
        """Check if the phonemizer is available"""
        # Always return True since we have a rule-based fallback
        return True
    
    @classmethod
    def is_supported_language(cls, language):
        """Check if language is supported"""
        return language.lower() in ["ur", "urdu"]

if __name__ == "__main__":
    # Test the AUTOMATIC three-tier phonemizer
    phonemizer = UrduPhonemizer()
    
    # You can add more custom phonemes if needed (optional)
    phonemizer.add_word_phoneme("جانا", "d͡ʒɑːnɑː")  # example: "go"
    
    test_texts = [
        "السلام علیکم",             # Will use CUSTOM_DICT
        "assalam u alaikum",        # Will use CUSTOM_DICT  
        "بسم اللہ الرحمن الرحیم",   # Mixed: CUSTOM_DICT + others
        "pakistan zindabad",        # CUSTOM_DICT + ESPEAK/RULE_BASED
        "یہ ایک ٹیسٹ ہے۔",         # Will use RULE_BASED
        "میں جا رہا ہوں"           # Mixed methods
    ]
    
    print(f"Supported languages: {phonemizer.supported_languages()}")
    print(f"Version: {phonemizer.version()}")
    print(f"Is available: {phonemizer.is_available()}")
    print("=" * 60)
    
    for text in test_texts:
        print(f"\n🔤 INPUT: '{text}'")
        result = phonemizer.phonemize(text, separator="|")
        print(f"🔊 OUTPUT: '{result}'")
        print("-" * 40)    print(f"Supported languages: {phonemizer.supported_languages()}")
    print(f"Version: {phonemizer.version()}")
    print(f"Is available: {phonemizer.is_available()}")
    print("=" * 60)
    
    for text in test_texts:
        print(f"\n🔤 INPUT: '{text}'")
        result = phonemizer.phonemize(text, separator="|")
        print(f"🔊 OUTPUT: '{result}'")
        print("-" * 40)
