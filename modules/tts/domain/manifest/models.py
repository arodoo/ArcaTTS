from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class BookType(Enum):
    """Type of literary work."""
    NOVEL = "novel"
    COLLECTION = "collection"
    SHORT_STORY = "short_story"
    ESSAY = "essay"


@dataclass
class Chapter:
    """Represents a chapter or story within a book."""
    number: int
    title: str
    start_line: int
    end_line: int
    text_content: str = ""
    
    @property
    def sanitized_title(self) -> str:
        """Clean title for filesystem usage."""
        clean = self.title.strip()
        clean = clean.replace(" ", "_")
        invalid = '<>:"/\\|?*'
        for char in invalid:
            clean = clean.replace(char, "")
        return clean[:50]


@dataclass
class Book:
    """Represents a complete book or collection."""
    number: int
    title: str
    year: Optional[int]
    book_type: BookType
    language: str = "es"
    chapters: List[Chapter] = field(default_factory=list)
    
    @property
    def sanitized_title(self) -> str:
        """Clean title for filesystem."""
        clean = self.title.strip()
        clean = clean.replace(" ", "_")
        invalid = '<>:"/\\|?*'
        for char in invalid:
            clean = clean.replace(char, "")
        return clean[:50]
    
    @property
    def folder_name(self) -> str:
        """Generate output folder name."""
        return f"{self.number:02d}-{self.sanitized_title}"
    
    def add_chapter(self, chapter: Chapter) -> None:
        """Add a chapter to the book."""
        self.chapters.append(chapter)
