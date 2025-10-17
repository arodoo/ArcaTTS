"""
Pause-Aware Text Chunker - Preserves punctuation pauses.
"""
from typing import List
import re


class PauseAwareChunker:
    """Split text without removing pause markers."""
    
    def __init__(self, max_chars: int = 500):
        self.max_chars = max_chars
    
    def chunk_text(self, text: str) -> List[str]:
        """Split at sentences, preserve spacing."""
        sentences = self._split_sentences(text)
        return self._group_sentences(sentences)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split at sentence boundaries."""
        pattern = r'(?<=[.!?])\s+'
        sentences = re.split(pattern, text)
        return [s for s in sentences if s.strip()]
    
    def _group_sentences(
        self, 
        sentences: List[str]
    ) -> List[str]:
        """Group without collapsing spaces."""
        chunks = []
        current = []
        current_len = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            
            if current_len + sentence_len > self.max_chars:
                if current:
                    chunks.append(" ".join(current))
                current = [sentence]
                current_len = sentence_len
            else:
                current.append(sentence)
                current_len += sentence_len
        
        if current:
            chunks.append(" ".join(current))
        
        return chunks
