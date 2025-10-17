from typing import List
import re


class TextChunker:
    """Split text into TTS-processable chunks."""
    
    def __init__(self, max_chars: int = 500):
        self.max_chars = max_chars
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text at sentence boundaries."""
        sentences = self._split_sentences(text)
        return self._group_sentences(sentences)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        pattern = r'(?<=[.!?])\s+'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _group_sentences(
        self, 
        sentences: List[str]
    ) -> List[str]:
        """Group sentences into chunks."""
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


class ChapterProcessor:
    """Process chapter text for TTS."""
    
    def __init__(self, chunk_size: int = 500):
        self.chunker = TextChunker(chunk_size)
    
    def prepare_chapter(
        self, 
        chapter_text: str
    ) -> List[str]:
        """Clean and chunk chapter text."""
        cleaned = self._clean_text(chapter_text)
        return self.chunker.chunk_text(cleaned)
    
    def _clean_text(self, text: str) -> str:
        """Remove formatting artifacts."""
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
