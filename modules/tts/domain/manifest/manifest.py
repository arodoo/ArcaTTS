from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
import json
from datetime import datetime
import re


@dataclass
class Work:
    """Represents a single literary work."""
    id: int
    title: str
    year: Optional[int]
    start_line: int
    end_line: int = 0
    text_content: str = ""
    chapters: List[str] = field(default_factory=list)
    
    @property
    def sanitized_title(self) -> str:
        """Clean title for filesystem."""
        clean = self.title.strip()
        clean = re.sub(r'[^\w\s-]', '', clean)
        clean = re.sub(r'[-\s]+', '_', clean)
        return clean[:50].upper()
    
    @property
    def folder_name(self) -> str:
        """Generate folder name."""
        return f"{self.id:02d}_{self.sanitized_title}"
    
    @property
    def estimated_lines(self) -> int:
        """Calculate work size."""
        return self.end_line - self.start_line
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "estimated_lines": self.estimated_lines,
            "folder_name": self.folder_name,
            "status": "pending"
        }


@dataclass
class Manifest:
    """Collection manifest with all works."""
    author: str
    source_file: str
    total_works: int
    works: List[Work] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Manifest':
        """Load from JSON dict."""
        works = [
            Work(
                id=w['id'],
                title=w['title'],
                year=w.get('year'),
                start_line=w['start_line'],
                end_line=w['end_line']
            )
            for w in data.get('works', [])
        ]
        
        return cls(
            author=data['author'],
            source_file=data['source_file'],
            total_works=data['total_works'],
            works=works,
            created_at=data.get('created_at', '')
        )
    
    def to_dict(self) -> Dict:
        """Convert to JSON."""
        return {
            "author": self.author,
            "source_file": self.source_file,
            "total_works": self.total_works,
            "created_at": self.created_at,
            "works": [w.to_dict() for w in self.works]
        }
    
    def save(self, output_path: Path) -> None:
        """Save manifest to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
