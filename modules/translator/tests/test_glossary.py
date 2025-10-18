"""
Unit tests for GlossaryService.
"""
import pytest
from modules.translator.domain.glossary_service import (
    GlossaryService
)


def test_glossary_extracts_proper_nouns():
    """Test proper noun extraction."""
    service = GlossaryService()
    original = "Franz Kafka escribió La Metamorfosis."
    translated = "Franz Kafka wrote The Metamorphosis."

    service.update_from_chunk(original, translated)

    assert "franz" in service.glossary
    assert service.glossary["franz"].target_term == "Franz"


def test_glossary_tracks_frequency():
    """Test term frequency tracking."""
    service = GlossaryService()

    service.update_from_chunk("Kafka said", "Kafka dijo")
    service.update_from_chunk("Kafka wrote", "Kafka escribió")

    assert service.glossary["kafka"].frequency == 2


def test_glossary_lookup():
    """Test term translation lookup."""
    service = GlossaryService()
    service.update_from_chunk("Paris", "París")

    result = service.get_term_translation("Paris")

    assert result == "París"
