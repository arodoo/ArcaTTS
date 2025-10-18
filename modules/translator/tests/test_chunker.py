"""
Unit tests for SemanticChunker.
"""
import pytest
from modules.translator.domain.chunker import SemanticChunker


def test_chunker_splits_paragraphs():
    """Test paragraph splitting."""
    text = "First paragraph.\n\nSecond paragraph."
    chunker = SemanticChunker(max_tokens=100)

    chunks = list(chunker.chunk_text(text))

    assert len(chunks) >= 2
    assert "First paragraph" in chunks[0]["text"]


def test_chunker_respects_token_limit():
    """Test token limit enforcement."""
    long_text = " ".join(["word"] * 1000)
    chunker = SemanticChunker(max_tokens=50)

    chunks = list(chunker.chunk_text(long_text))

    assert len(chunks) > 1


def test_chunker_preserves_context():
    """Test context extraction."""
    text = "Para 1.\n\nPara 2.\n\nPara 3."
    chunker = SemanticChunker(
        max_tokens=100,
        context_sentences=1
    )

    chunks = list(chunker.chunk_text(text))

    for chunk in chunks[1:]:
        assert chunk["context_before"]
