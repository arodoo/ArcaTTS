import re
from typing import List, Tuple
from pathlib import Path
from modules.tts.domain.manifest import Work, Manifest


class ManifestParser:
    """Parse book file and generate manifest."""
    
    INDEX_START = "ÍNDICE"
    INDEX_END = "FIN DEL ÍNDICE"
    WORK_MARKER = "$"
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lines: List[str] = []
        self.author = self._extract_author()
    
    def _extract_author(self) -> str:
        """Extract author from filename."""
        name = self.file_path.stem
        name = name.replace('-', ' ').replace('_', ' ')
        return name.title()
    
    def parse(self) -> Manifest:
        """Parse file and create manifest."""
        self._load_file()
        index_works = self._extract_index()
        works = self._find_work_boundaries(index_works)
        
        manifest = Manifest(
            author=self.author,
            source_file=str(self.file_path),
            total_works=len(works),
            works=works
        )
        
        return manifest
    
    def _load_file(self) -> None:
        """Load file into memory."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
    
    def _extract_index(self) -> List[Tuple[str, int]]:
        """Extract work titles from index section."""
        works = []
        in_index = False
        
        for line_num, line in enumerate(self.lines, 1):
            line_stripped = line.strip()
            
            if self.INDEX_START in line_stripped:
                in_index = True
                continue
            
            if self.INDEX_END in line_stripped:
                break
            
            if in_index and line_stripped.startswith(self.WORK_MARKER):
                title = line_stripped[1:].strip()
                year = self._extract_year(title)
                
                if year:
                    title = re.sub(r'\s*\(\d{4}\)\s*$', '', title)
                
                works.append((title, year))
        
        return works
    
    def _extract_year(self, title: str) -> int:
        """Extract year from title."""
        match = re.search(r'\((\d{4})\)', title)
        return int(match.group(1)) if match else None
    
    def _find_work_boundaries(
        self, 
        index_works: List[Tuple[str, int]]
    ) -> List[Work]:
        """Find and order works by position."""
        works = []
        seen_lines = set()
        
        for title, year in index_works:
            start_line = self._find_work_start(title)
            
            if start_line and start_line not in seen_lines:
                work = Work(
                    id=0,
                    title=title,
                    year=year,
                    start_line=start_line
                )
                works.append(work)
                seen_lines.add(start_line)
        
        works.sort(key=lambda w: w.start_line)
        
        for i, work in enumerate(works, 1):
            work.id = i
        
        for i in range(len(works) - 1):
            works[i].end_line = works[i + 1].start_line - 1
        
        if works:
            works[-1].end_line = len(self.lines)
        
        return works
    
    def _find_work_start(self, title: str) -> int:
        """Find work start (standalone title)."""
        title_clean = title.upper().strip()
        
        for line_num, line in enumerate(self.lines, 1):
            if line_num < 100:
                continue
            
            line_clean = line.strip().upper()
            
            if not line_clean:
                continue
            
            if line_clean == title_clean:
                return line_num
        
        return None
