# Grammar Checker - Singleton
# Prevents multiple LanguageTool downloads

import language_tool_python
from modules.grammar.domain.models import (
    GrammarError,
    ErrorType,
    Severity
)
from typing import List, Optional


# Global singleton - created once
_GLOBAL_TOOL = None


def get_checker(language: str = "es"):
    """Get singleton LanguageTool instance."""
    global _GLOBAL_TOOL
    if _GLOBAL_TOOL is None:
        _GLOBAL_TOOL = language_tool_python.LanguageTool(
            language
        )
    return _GLOBAL_TOOL


class GrammarChecker:
    """Grammar checker using singleton."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.tool = get_checker(language)
    
    def check_text(
        self, 
        text: str, 
        line_offset: int = 0
    ) -> List[GrammarError]:
        """Check text for grammar errors."""
        matches = self.tool.check(text)
        
        errors = []
        for match in matches:
            error = self._convert_match(
                match, 
                line_offset
            )
            errors.append(error)
        
        return errors
