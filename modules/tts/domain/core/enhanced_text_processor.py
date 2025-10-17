"""
Enhanced Text Processor - With pauses and conversions.
"""
from typing import List
import re
from ..text.pause_aware_chunker import PauseAwareChunker
from ..text.roman_converter import RomanConverter
from ..audio.silence_generator import SilenceGenerator
from ..text.punctuation_pauser import PunctuationPauser
from ..text.hyphenation_resolver import HyphenationResolver


class EnhancedTextProcessor:
    """Process text with title pauses and Roman conversion."""
    
    def __init__(self, chunk_size: int = 500):
        self.chunker = PauseAwareChunker(chunk_size)
        self.roman = RomanConverter()
        self.silence = SilenceGenerator()
        self.pauser = PunctuationPauser()
        self.hyphenation = HyphenationResolver()
    
    def prepare_work_text(
        self, 
        text: str,
        add_title_pause: bool = True
    ) -> List[str]:
        """
        Process work text with minimal intervention.
        Let Piper handle pauses naturally.
        """
        text = self.hyphenation.resolve(text)
        text = self._remove_leading_ellipsis(text)
        
        if add_title_pause:
            text = self._add_title_pause(text)
        
        # Convert Roman numerals
        text = self.roman.convert_line(text)
        
        # Normalize newlines
        text = self._normalize_newlines(text)
        
        # Only add prosodic markers (no pause conversion)
        text = self.pauser.add_pauses(text)
        
        # Chunk text (only on long silences)
        chunks = self._chunk_with_silences(text)
        
        return chunks
    
    def _remove_leading_ellipsis(self, text: str) -> str:
        """Remove leading ellipsis from lines (editorial markers)."""
        import re
        # Only remove the '...' at start of lines, keep the rest
        text = re.sub(r'^\.\.\.', '', text, flags=re.MULTILINE)
        return text
    
    def _normalize_newlines(self, text: str) -> str:
        """Replace single newlines with spaces, keep paragraphs."""
        import re
        # First, protect paragraph breaks (2+ newlines)
        text = re.sub(r'\n\n+', '<!PARAGRAPH!>', text)
        # Replace single newlines with space
        text = text.replace('\n', ' ')
        # Restore paragraph breaks
        text = text.replace('<!PARAGRAPH!>', '\n\n')
        return text
    
    def _add_title_pause(self, text: str) -> str:
        """Add pause after first line (title)."""
        lines = text.split('\n', 1)
        
        if len(lines) < 2:
            return text
        
        title = lines[0].strip()
        rest = lines[1].lstrip() if len(lines) > 1 else ""
        
        return f"{title}<silence:2.0>{rest}"
    
    def _chunk_with_silences(
        self, 
        text: str
    ) -> List[str]:
        """Chunk text, only split on LONG silences (>=1s).
        
        Short pauses (punctuation) stay within text chunks.
        This prevents excessive fragmentation.
        """
        # Only split on long silences (title, paragraph breaks)
        long_silence_pattern = r'<silence:([1-9]\d*\.?\d*)>'
        parts = re.split(long_silence_pattern, text)
        
        chunks = []
        i = 0
        while i < len(parts):
            part = parts[i]
            
            # Check if this is a duration (from split group)
            if i > 0 and re.match(r'[1-9]\d*\.?\d*', part):
                # This is a silence duration
                chunks.append(f"<silence:{part}>")
                i += 1
            else:
                # This is text (may contain short silences)
                if part.strip():
                    chunks.extend(self.chunker.chunk_text(part))
                i += 1
        
        return [c for c in chunks if c.strip()]
