from datetime import datetime
from pathlib import Path
from typing import Optional


class VersionManager:
    """Manages file versioning for corrections."""
    
    @staticmethod
    def generate_version() -> str:
        """Generate timestamp-based version."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def create_versioned_filename(
        original_path: str,
        version: Optional[str] = None
    ) -> Path:
        """
        Create versioned filename.
        Example: franz-kafka.txt -> 
                 franz-kafka_v20251012_143022.txt
        """
        path = Path(original_path)
        if version is None:
            version = VersionManager.generate_version()
        
        stem = path.stem
        suffix = path.suffix
        
        versioned = f"{stem}_v{version}{suffix}"
        return Path(versioned)
    
    @staticmethod
    def create_summary_filename(
        original_path: str,
        version: Optional[str] = None
    ) -> Path:
        """
        Create summary filename.
        Example: franz-kafka_fixes_v20251012_143022.json
        """
        path = Path(original_path)
        if version is None:
            version = VersionManager.generate_version()
        
        stem = path.stem
        summary = f"{stem}_fixes_v{version}.json"
        return Path(summary)
