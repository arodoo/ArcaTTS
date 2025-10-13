import language_tool_python
from typing import List, Optional
from modules.grammar.domain.models import (
    GrammarError,
    ErrorType,
    Severity
)
import time


class GrammarChecker:
    """Grammar checker using LanguageTool."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.tool = None
    
    def _init_tool(self) -> None:
        """Lazy initialization with retry."""
        if self.tool is None:
            for attempt in range(3):
                try:
                    self.tool = (
                        language_tool_python.LanguageTool(
                            self.language,
                            remote_server=None
                        )
                    )
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        raise
    
    def check_text(
        self, 
        text: str, 
        line_offset: int = 0
    ) -> List[GrammarError]:
        """Check text for grammar errors."""
        self._init_tool()
        matches = self.tool.check(text)
        
        errors = []
        for match in matches:
            error = self._convert_match(
                match, 
                line_offset
            )
            errors.append(error)
        
        return errors
    
    def _convert_match(
        self, 
        match, 
        line_offset: int
    ) -> GrammarError:
        """Convert LanguageTool match to GrammarError."""
        error_type = self._get_error_type(
            match.ruleIssueType
        )
        severity = self._get_severity(match)
        
        return GrammarError(
            line_number=line_offset,
            offset=match.offset,
            length=match.errorLength,
            error_type=error_type,
            severity=severity,
            message=match.message,
            original_text=match.context,
            suggested_replacement=self._get_suggestion(
                match
            ),
            rule_id=match.ruleId
        )
    
    def _get_error_type(
        self, 
        issue_type: Optional[str]
    ) -> ErrorType:
        """Map LanguageTool type to ErrorType."""
        if not issue_type:
            return ErrorType.GRAMMAR
        
        type_map = {
            "misspelling": ErrorType.SPELLING,
            "typographical": ErrorType.TYPOGRAPHY,
            "grammar": ErrorType.GRAMMAR,
            "punctuation": ErrorType.PUNCTUATION,
            "style": ErrorType.STYLE
        }
        
        return type_map.get(
            issue_type.lower(), 
            ErrorType.GRAMMAR
        )
    
    def _get_severity(self, match) -> Severity:
        """Determine error severity."""
        if hasattr(match, 'category'):
            if "TYPOS" in match.category:
                return Severity.HIGH
        return Severity.MEDIUM
    
    def _get_suggestion(self, match) -> Optional[str]:
        """Extract first suggestion if available."""
        if match.replacements:
            return match.replacements[0]
        return None
    
    def close(self) -> None:
        """Close LanguageTool connection."""
        if self.tool:
            self.tool.close()
