"""
Disk-based translation cache.
Stores translations as JSON files.
"""
import json
from pathlib import Path
from typing import Optional
from uuid import UUID

from ..domain.repository import ITranslationRepository
from ..domain.translation import Translation
from .serializer import CacheSerializer
from .deserializer import CacheDeserializer


class DiskCacheRepository(ITranslationRepository):
    """File system translation storage."""

    def __init__(self, cache_dir: str = ".cache/translations"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.serializer = CacheSerializer()
        self.deserializer = CacheDeserializer()

    def save(self, translation: Translation) -> None:
        """Save to disk as JSON."""
        file_path = self._get_path(translation.translation_id)
        data = self.serializer.serialize(translation)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_by_id(
        self,
        translation_id: UUID
    ) -> Optional[Translation]:
        """Load from disk."""
        file_path = self._get_path(translation_id)

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return self.deserializer.deserialize(data)

    def delete(self, translation_id: UUID) -> None:
        """Remove file."""
        file_path = self._get_path(translation_id)
        if file_path.exists():
            file_path.unlink()

    def exists(self, translation_id: UUID) -> bool:
        """Check file exists."""
        return self._get_path(translation_id).exists()

    def _get_path(self, translation_id: UUID) -> Path:
        """Get file path for ID."""
        return self.cache_dir / f"{translation_id}.json"
