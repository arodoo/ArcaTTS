"""
Validation orchestration service.
Combines all validators.
"""
from ..domain.value_objects import ValidationScore
from ..domain.validators import LengthValidator
from ..domain.number_validator import NumberValidator


class ValidationService:
    """Run all validations on translation."""

    def __init__(self):
        self.length_validator = LengthValidator()
        self.number_validator = NumberValidator()

    def validate(
        self,
        original: str,
        translated: str
    ) -> ValidationScore:
        """Run all checks and combine scores."""
        length_result = self.length_validator.validate(
            original,
            translated
        )
        number_result = self.number_validator.validate(
            original,
            translated
        )

        combined_score = (
            length_result.score * 0.4 +
            number_result.score * 0.6
        )

        all_issues = (
            length_result.issues +
            number_result.issues
        )

        is_valid = (
            length_result.is_valid and
            number_result.is_valid
        )

        return ValidationScore(
            is_valid=is_valid,
            score=combined_score,
            issues=all_issues
        )
