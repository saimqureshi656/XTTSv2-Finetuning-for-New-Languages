from typing import Dict
from TTS.tts.utils.text.urdu.phonemizer import urdu_text_to_phonemes, normalize_urdu_text
from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_UR_PUNCS = "۔؍،؞؎؏؋٭٪٬٫"  # Urdu punctuation marks


class UrduPhonemizer(BasePhonemizer):
    """🐸TTS Urdu phonemizer using espeak-ng and rule-based fallback

    This phonemizer converts Urdu text to IPA phonemes using:
    1. Primary: espeak-ng with Urdu voice
    2. Fallback: Rule-based Urdu to IPA conversion

    Example:
        >>> from TTS.tts.utils.text.phonemizers import UrduPhonemizer
        >>> phonemizer = UrduPhonemizer()
        >>> phonemizer.phonemize("یہ ایک اردو جملہ ہے۔", separator="|")
        'j|eː|ɦ| |eː|k| |ʊ|r|d̪|uː| |d͡ʒ|ʊ|m|l|ɑː| |ɦ|eː|۔'
    """

    language = "ur"

    def __init__(self, punctuations=_DEF_UR_PUNCS, keep_puncs=True, use_espeak=True, **kwargs):
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)
        self.use_espeak = use_espeak

    @staticmethod
    def name():
        return "urdu_phonemizer"

    def _phonemize(self, text: str, separator: str = "|") -> str:
        """Convert Urdu text to IPA phonemes"""
        # Normalize text first
        text = normalize_urdu_text(text)
        
        # Get phonemes
        phonemes = urdu_text_to_phonemes(text, use_espeak=self.use_espeak)
        
        # Apply separator if specified
        if separator and separator != "":
            # Split phonemes and join with separator
            phoneme_chars = list(phonemes.replace(' ', f' {separator}'))
            return separator.join(phoneme_chars)
        
        return phonemes

    def phonemize(self, text: str, separator: str = "|", language=None) -> str:
        """Public phonemization method"""
        return self._phonemize(text, separator)

    @staticmethod
    def supported_languages() -> Dict:
        return {"ur": "urdu"}

    def version(self) -> str:
        return "1.0.0"

    def is_available(self) -> bool:
        """Check if the phonemizer is available"""
        try:
            # Test basic functionality
            test_result = urdu_text_to_phonemes("ٹیسٹ", use_espeak=self.use_espeak)
            return bool(test_result)
        except Exception:
            return False


if __name__ == "__main__":
    # Test the phonemizer
    phonemizer = UrduPhonemizer()
    #test_texts = [
       # "سلام علیکم",
       # "یہ ایک ٹیسٹ ہے۔",
       # "اردو زبان بہت خوبصورت ہے۔"
   # ]
    
    print(f"Supported languages: {phonemizer.supported_languages()}")
    print(f"Version: {phonemizer.version()}")
    print(f"Is available: {phonemizer.is_available()}")
    
    for text in test_texts:
        result = phonemizer.phonemize(text, separator="|")
        print(f"'{text}' -> '{result}'")
