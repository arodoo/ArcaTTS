"""
Number and term consistency validators.
Additional validation rules.
"""
import re

from ..domain.value_objects import ValidationScore


class NumberValidator:
    """Ensure numbers are preserved."""

    def validate(
        self,
        original: str,
        translated: str
    ) -> ValidationScore:
        """Check number consistency."""
        orig_nums = set(
            re.findall(r'\b\d+(?:[.,]\d+)?\b', original)
        )
        trans_nums = set(
            re.findall(r'\b\d+(?:[.,]\d+)?\b', translated)
        )

        if orig_nums == trans_nums:
            return ValidationScore(
                is_valid=True,
                score=1.0,
                issues=()
            )

        missing = orig_nums - trans_nums
        extra = trans_nums - orig_nums

        issues = []
        if missing:
            issues.append(f"Missing numbers: {missing}")
        if extra:
            issues.append(f"Extra numbers: {extra}")

        return ValidationScore(
            is_valid=False,
            score=0.5,
            issues=tuple(issues)
        )
