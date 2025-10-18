"""
Celery tasks for async translation.
"""
from celery import Task
from typing import Optional

from ..infrastructure.m2m100_adapter import (
    M2M100Adapter
)
from ..application.translation_service import (
    TranslationService
)
from ..infrastructure.disk_cache import DiskCacheRepository


class TranslationTask(Task):
    """Base task with shared resources."""

    _translator = None
    _service = None
    _cache = None

    @property
    def translator(self):
        """Lazy load translator."""
        if self._translator is None:
            self._translator = M2M100Adapter(
                use_gpu=True,
                model_size="418M"
            )
        return self._translator

    @property
    def service(self):
        """Lazy load service."""
        if self._service is None:
            self._service = TranslationService(
                self.translator
            )
        return self._service

    @property
    def cache(self):
        """Lazy load cache."""
        if self._cache is None:
            self._cache = DiskCacheRepository()
        return self._cache
