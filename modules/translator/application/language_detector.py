"""
Language detection service.
Identifies source text language.
"""
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class LanguageDetector:
    """Detect text language."""

    SUPPORTED_LANGUAGES = {
        'en', 'es', 'fr', 'de', 'it', 'pt'
    }

    def detect_language(self, text: str) -> str:
        """Detect language code."""
        if not text or len(text.strip()) < 10:
            raise ValueError("Text too short for detection")

        detected = detect(text)

        if detected not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {detected}"
            )

        return detected

    def is_supported(self, language_code: str) -> bool:
        """Check if language is supported."""
        return language_code in self.SUPPORTED_LANGUAGES
