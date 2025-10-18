"""
Unit tests for validators.
"""
import pytest
from modules.translator.domain.validators import (
    LengthValidator
)
from modules.translator.domain.number_validator import (
    NumberValidator
)


def test_length_validator_accepts_normal_ratio():
    """Test acceptable length ratio."""
    validator = LengthValidator()
    original = "This is a test sentence."
    translated = "Esta es una oración de prueba."

    result = validator.validate(original, translated)

    assert result.is_valid
    assert result.score > 0.7


def test_length_validator_rejects_extreme_ratio():
    """Test rejection of extreme ratios."""
    validator = LengthValidator()
    original = "Hello"
    translated = "A very long translation " * 10

    result = validator.validate(original, translated)

    assert not result.is_valid


def test_number_validator_preserves_numbers():
    """Test number preservation."""
    validator = NumberValidator()
    original = "There are 42 cats and 7 dogs."
    translated = "Hay 42 gatos y 7 perros."

    result = validator.validate(original, translated)

    assert result.is_valid
    assert result.score == 1.0


def test_number_validator_detects_missing():
    """Test missing number detection."""
    validator = NumberValidator()
    original = "The year 2024 was great."
    translated = "El año fue genial."

    result = validator.validate(original, translated)

    assert not result.is_valid
