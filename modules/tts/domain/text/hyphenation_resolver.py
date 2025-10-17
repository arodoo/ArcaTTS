"""
Hyphenation Resolver - Fix word breaks at line ends.
"""
import re


class HyphenationResolver:
    """Join hyphenated words split across lines."""
    
    CONTINUATION_MARKERS = [
        '¬',   # OCR hyphenation
        '-',   # Standard hyphen
        '=',   # Old format hyphenation
    ]
    
    def resolve(self, text: str) -> str:
        """Fix hyphenated words."""
        result = text
        
        result = self._fix_negation_symbol(result)
        result = self._fix_end_of_line_hyphens(result)
        
        return result
    
    def _fix_negation_symbol(self, text: str) -> str:
        """Replace ¬ at line breaks."""
        pattern = r'¬\s*\n\s*'
        return re.sub(pattern, '', text)
    
    def _fix_end_of_line_hyphens(self, text: str) -> str:
        """Join words split with hyphen at EOL.
        
        Rules:
        1. Lowercase before hyphen + newline + lowercase = join
        2. Otherwise preserve hyphen (dialogue, compounds)
        """
        pattern = r'([a-záéíóúñü])-\s*\n\s*([a-záéíóúñü])'
        
        def replace_func(match):
            return match.group(1) + match.group(2)
        
        return re.sub(pattern, replace_func, text, flags=re.IGNORECASE)
    
    def preserve_dialogue_hyphens(self, text: str) -> str:
        """Ensure dialogue hyphens stay intact."""
        text = re.sub(r'\n\s*—', '\n—', text)
        text = re.sub(r'—\s*\n', '—\n', text)
        return text
