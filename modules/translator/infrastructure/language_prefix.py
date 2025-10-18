"""
Language prefix handler for multilingual models.
Adds target language tags for itc-itc model.
"""
from ..domain.value_objects import LanguagePair


class LanguagePrefixHandler:
    """Handle language prefixes for multilingual models."""

    LANGUAGE_CODES = {
        "es": ">>spa<<",
        "pt": ">>por<<",
        "fr": ">>fra<<",
        "it": ">>ita<<",
        "ro": ">>ron<<",
        "ca": ">>cat<<",
    }

    @staticmethod
    def needs_prefix(model_name: str) -> bool:
        """Check if model requires language prefix."""
        return "itc-itc" in model_name or "roa" in model_name

    @staticmethod
    def add_prefix(
        text: str,
        language_pair: LanguagePair,
        model_name: str
    ) -> str:
        """Add target language prefix if needed."""
        if not LanguagePrefixHandler.needs_prefix(model_name):
            return text

        target_code = LanguagePrefixHandler.LANGUAGE_CODES.get(
            language_pair.target
        )

        if target_code:
            return f"{target_code} {text}"

        return text
