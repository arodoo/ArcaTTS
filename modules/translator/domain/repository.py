"""
Translation cache repository interface.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..domain.translation import Translation


class ITranslationRepository(ABC):
    """Repository contract for translations."""

    @abstractmethod
    def save(self, translation: Translation) -> None:
        """Persist translation."""
        pass

    @abstractmethod
    def get_by_id(
        self,
        translation_id: UUID
    ) -> Optional[Translation]:
        """Retrieve by ID."""
        pass

    @abstractmethod
    def delete(self, translation_id: UUID) -> None:
        """Remove translation."""
        pass

    @abstractmethod
    def exists(self, translation_id: UUID) -> bool:
        """Check if exists."""
        pass
