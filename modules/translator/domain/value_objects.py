"""
Value objects for translation domain.
Immutable, equality by value.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LanguagePair:
    """Language pair for translation."""
    source: str
    target: str

    def __post_init__(self):
        if not self.source or not self.target:
            raise ValueError("Languages required")
        if self.source == self.target:
            raise ValueError("Same language pair")


@dataclass(frozen=True)
class ValidationScore:
    """Quality validation score."""
    is_valid: bool
    score: float
    issues: tuple[str, ...]

    def __post_init__(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Score must be 0-1")
