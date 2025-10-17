"""
Work Processor - Extract and process works.
"""
from pathlib import Path
from typing import List
import json

from .manifest import Work


class WorkExtractor:
    """Extract work content from source."""
    
    def __init__(self, source_file: str):
        self.source_file = Path(source_file)
        self.lines = self._load_lines()
    
    def _load_lines(self) -> List[str]:
        """Load all lines."""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.readlines()
    
    def extract(self, work: Work) -> str:
        """Extract work text with title."""
        # start_line points to title in file, skip it
        # Skip title line + empty line after it
        start = work.start_line + 1
        end = work.end_line
        
        content_lines = self.lines[start:end]
        
        # Prepend title for TTS processing
        title_line = work.title + '\n'
        content = title_line + ''.join(content_lines)
        
        return content
    
    def save_work(self, work: Work, output_dir: Path):
        """Save work to individual file."""
        work_dir = output_dir / work.folder_name
        work_dir.mkdir(parents=True, exist_ok=True)
        
        work_file = work_dir / "text.txt"
        content = self.extract(work)
        
        with open(work_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        meta_file = work_dir / "metadata.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(work.to_dict(), f, indent=2)
        
        return work_file
