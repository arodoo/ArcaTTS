import re
from typing import List, Tuple
from modules.tts.domain.models import Book, Chapter, BookType


class BookStructureParser:
    """Parse book file structure and metadata."""
    
    BOOK_PATTERN = r'^([A-ZÁÉÍÓÚÑ\s]+)\((\d{4})\)\s*$'
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines: List[str] = []
        self._load_file()
    
    def _load_file(self) -> None:
        """Load file content into memory."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
    
    def extract_index(self) -> List[Tuple[str, int]]:
        """Extract book titles and years from index."""
        books = []
        pattern = re.compile(self.BOOK_PATTERN)
        
        for line_num, line in enumerate(self.lines[:300]):
            match = pattern.match(line.strip())
            if match:
                title = match.group(1).strip()
                year = int(match.group(2))
                books.append((title, year, line_num))
        
        return books
    
    def detect_book_type(
        self, 
        title: str, 
        content_preview: str
    ) -> BookType:
        """Determine if book is novel or collection."""
        novels = [
            "AMERICA", "METAMORFOSIS", "PROCESO", 
            "CASTILLO", "CARTA AL PADRE"
        ]
        
        for novel in novels:
            if novel in title.upper():
                return BookType.NOVEL
        
        return BookType.COLLECTION
    
    def find_book_boundaries(
        self, 
        book_title: str, 
        start_line: int
    ) -> Tuple[int, int]:
        """Find start and end lines for a book."""
        end_line = len(self.lines)
        
        pattern = re.compile(self.BOOK_PATTERN)
        for i in range(start_line + 1, len(self.lines)):
            if pattern.match(self.lines[i].strip()):
                end_line = i
                break
        
        return start_line, end_line
