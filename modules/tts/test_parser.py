"""
Quick test of the book structure parser.
Run from repository root: python -m modules.tts.test_parser
"""
import sys
from pathlib import Path

# Add root to path for imports
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from modules.tts.domain.parser import BookStructureParser


def main():
    # Path relative to repo root
    book_path = root / "boocks" / "franz-kafka.txt"
    parser = BookStructureParser(str(book_path))
    
    print("=" * 60)
    print("BOOK STRUCTURE ANALYSIS")
    print("=" * 60)
    
    books = parser.extract_index()
    
    print(f"\nFound {len(books)} books:\n")
    
    for idx, (title, year, line_num) in enumerate(books, 1):
        print(f"{idx:02d}. {title} ({year}) "
              f"[Line {line_num}]")
        
        start, end = parser.find_book_boundaries(
            title, 
            line_num
        )
        lines_count = end - start
        
        book_type = parser.detect_book_type(
            title, 
            ""
        )
        
        print(f"    Type: {book_type.value}")
        print(f"    Lines: {start} to {end} "
              f"({lines_count} lines)")
        print()


if __name__ == "__main__":
    main()
