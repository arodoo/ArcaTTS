"""
Translation validators.
Check quality and consistency of translations.
"""
from ..domain.value_objects import ValidationScore


class LengthValidator:
    """Validate relative length of translation."""

    MAX_RATIO = 2.5
    MIN_RATIO = 0.4

    def validate(
        self,
        original: str,
        translated: str
    ) -> ValidationScore:
        """Check length is reasonable."""
        orig_len = len(original.split())
        trans_len = len(translated.split())

        if orig_len == 0:
            return ValidationScore(
                is_valid=False,
                score=0.0,
                issues=("Empty original text",)
            )

        ratio = trans_len / orig_len

        if self.MIN_RATIO <= ratio <= self.MAX_RATIO:
            score = 1.0 - abs(1.0 - ratio) / 2
            return ValidationScore(
                is_valid=True,
                score=score,
                issues=()
            )

        return ValidationScore(
            is_valid=False,
            score=0.3,
            issues=(f"Length ratio {ratio:.2f} suspicious",)
        )
