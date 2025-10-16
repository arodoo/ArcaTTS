from typing import List, Optional, Dict
from modules.grammar.domain.models import (
    GrammarError,
    ErrorType,
    Severity
)
from modules.grammar.domain.lt_local import (
    LanguageToolLocal
)


# Global singleton instances per language
_TOOL_INSTANCES: Dict[str, any] = {}


class GrammarChecker:
    """Grammar checker using LanguageTool."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.tool = None
    
    def _init_tool(self) -> None:
        """Initialize local LanguageTool."""
        if self.tool is None:
            if self.language not in _TOOL_INSTANCES:
                _TOOL_INSTANCES[self.language] = (
                    LanguageToolLocal(self.language)
                )
            self.tool = _TOOL_INSTANCES[self.language]
    
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
        match: dict, 
        line_offset: int
    ) -> GrammarError:
        """Convert JSON match to GrammarError."""
        issue_type = match.get('rule', {}).get(
            'issueType'
        )
        error_type = self._get_error_type(issue_type)
        severity = self._get_severity(match)
        
        # Get first replacement if available
        replacements = match.get('replacements', [])
        suggestion = None
        if replacements:
            suggestion = replacements[0].get('value')
        
        return GrammarError(
            line_number=line_offset,
            offset=match.get('offset', 0),
            length=match.get('length', 0),
            error_type=error_type,
            severity=severity,
            message=match.get('message', ''),
            original_text=match.get('context', {}).get(
                'text', ''
            ),
            suggested_replacement=suggestion,
            rule_id=match.get('rule', {}).get(
                'id', ''
            )
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
    
    def _get_severity(self, match: dict) -> Severity:
        """Determine error severity from JSON."""
        category = match.get('rule', {}).get(
            'category', {}
        ).get('id', '')
        
        if "TYPOS" in category:
            return Severity.HIGH
        return Severity.MEDIUM
    
    def _get_suggestion(
        self, 
        match: dict
    ) -> Optional[str]:
        """Extract first suggestion if available."""
        replacements = match.get('replacements', [])
        if replacements:
            return replacements[0].get('value')
        return None
