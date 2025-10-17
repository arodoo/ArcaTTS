"""
Chapter Detector - Find chapter boundaries in works.
"""
import re
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Chapter:
    """Chapter information."""
    number: int
    roman: str
    start_line: int
    end_line: int = 0
    
    @property
    def folder_name(self) -> str:
        """Generate folder name."""
        return f"capitulo_{self.number:02d}"


class ChapterDetector:
    """Detect chapters in long works."""
    
    ROMAN_PATTERN = r'^\s*([IVX]+)\s*$'
    MIN_CHAPTER_LINES = 100
    
    def detect_chapters(
        self, 
        text: str
    ) -> List[Chapter]:
        """Find chapter markers."""
        lines = text.split('\n')
        chapters = []
        
        for i, line in enumerate(lines):
            match = re.match(self.ROMAN_PATTERN, line.strip())
            
            if match:
                roman = match.group(1)
                number = self._roman_to_int(roman)
                
                if number:
                    chapters.append(Chapter(
                        number=number,
                        roman=roman,
                        start_line=i
                    ))
        
        for i in range(len(chapters) - 1):
            chapters[i].end_line = chapters[i + 1].start_line
        
        if chapters:
            chapters[-1].end_line = len(lines)
        
        return [c for c in chapters 
                if c.end_line - c.start_line > self.MIN_CHAPTER_LINES]
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman to integer."""
        values = {'I': 1, 'V': 5, 'X': 10}
        result = 0
        prev = 0
        
        for char in reversed(roman):
            val = values.get(char, 0)
            if val < prev:
                result -= val
            else:
                result += val
            prev = val
        
        return result if result > 0 else None
