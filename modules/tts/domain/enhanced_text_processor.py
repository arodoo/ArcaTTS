"""
Enhanced Text Processor - With pauses and conversions.
"""
from typing import List
from .pause_aware_chunker import PauseAwareChunker
from .roman_converter import RomanConverter
from .silence_generator import SilenceGenerator
from .punctuation_pauser import PunctuationPauser
from .hyphenation_resolver import HyphenationResolver


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
        """Process work text with enhancements."""
        text = self.hyphenation.resolve(text)
        
        if add_title_pause:
            text = self._add_title_pause(text)
        
        text = self.roman.convert_line(text)
        text = self.pauser.convert_to_piper_format(
            self.pauser.add_pauses(text)
        )
        
        chunks = self._chunk_with_silences(text)
        
        return chunks
    
    def _add_title_pause(self, text: str) -> str:
        """Add pause after first line (title)."""
        lines = text.split('\n', 1)
        
        if len(lines) < 2:
            return text
        
        title = lines[0].strip()
        rest = lines[1] if len(lines) > 1 else ""
        
        return f"{title}\n<silence:2.0>\n{rest}"
    
    def _chunk_with_silences(
        self, 
        text: str
    ) -> List[str]:
        """Chunk text preserving silence markers."""
        parts = text.split('<silence:')
        chunks = []
        
        for i, part in enumerate(parts):
            if i == 0:
                chunks.extend(self.chunker.chunk_text(part))
            else:
                duration_end = part.find('>')
                if duration_end > 0:
                    duration = part[:duration_end]
                    rest = part[duration_end + 1:]
                    
                    chunks.append(f"<silence:{duration}>")
                    
                    if rest.strip():
                        chunks.extend(
                            self.chunker.chunk_text(rest)
                        )
        
        return [c for c in chunks if c.strip()]
