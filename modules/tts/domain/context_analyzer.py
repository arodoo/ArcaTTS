import re
from typing import Literal


ContextType = Literal[
    "question", "exclamation", "dialogue",
    "narrative", "pause"
]


class ContextAnalyzer:
    """Analyzes text for optimal synthesis params."""
    
    QUESTION_WORDS = {
        "qué", "quién", "cuándo", "dónde",
        "cómo", "por qué", "cuál", "cuáles"
    }
    
    EXCLAMATION_WORDS = {
        "ay", "oh", "ah", "eh", "uf",
        "caramba", "dios", "cielos"
    }
    
    def analyze(self, text: str) -> ContextType:
        """Determine text context type."""
        t = text.lower().strip()
        
        if "¿" in t or t.endswith("?"):
            return "question"
        if "¡" in t or t.endswith("!"):
            return "exclamation"
        if text.startswith(("—", "-")):
            return "dialogue"
        if text.strip() in ["...", "…", ""]:
            return "pause"
        
        words = t.split()
        if words:
            if words[0] in self.QUESTION_WORDS:
                return "question"
            if words[0] in self.EXCLAMATION_WORDS:
                return "exclamation"
        
        return "narrative"
