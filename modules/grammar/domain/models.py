from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ErrorType(Enum):
    """Types of grammar errors."""
    SPELLING = "spelling"
    GRAMMAR = "grammar"
    PUNCTUATION = "punctuation"
    TYPOGRAPHY = "typography"
    STYLE = "style"


class Severity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class GrammarError:
    """Represents a detected grammar error."""
    line_number: int
    offset: int
    length: int
    error_type: ErrorType
    severity: Severity
    message: str
    original_text: str
    suggested_replacement: Optional[str] = None
    rule_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "line": self.line_number,
            "offset": self.offset,
            "length": self.length,
            "type": self.error_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "original": self.original_text,
            "suggested": self.suggested_replacement,
            "rule": self.rule_id
        }


@dataclass
class CorrectionResult:
    """Result of grammar correction process."""
    original_file: str
    corrected_file: str
    total_errors: int
    fixed_errors: int
    errors: List[GrammarError]
    success: bool = True
    error_message: Optional[str] = None
