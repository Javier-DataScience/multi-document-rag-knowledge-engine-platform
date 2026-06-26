# ==========================================================
# FILE: test_chunker.py
#
# PURPOSE:
# Unit tests for the semantic chunking module.
#
# RESPONSIBILITY:
# Verify that chunking behaves correctly and produces
# valid outputs.
#
# TEST STRATEGY:
# - Ensure output is a list
# - Ensure chunks are generated
# - Ensure chunks are not empty
# - Ensure chunks respect the maximum size
#
# ARCHITECTURAL ROLE:
# This is our first automated pytest unit test and forms
# the foundation for CI/CD later in the project.
# ==========================================================

from app.ingestion.chunker import chunk_text


def test_chunker_returns_list():
    """
    The chunker should always return a Python list.
    """

    text = "Machine learning is amazing."

    chunks = chunk_text(text)

    assert isinstance(chunks, list)


def test_chunker_generates_chunks():
    """
    The chunker should generate at least one chunk.
    """

    text = "Machine learning is amazing."

    chunks = chunk_text(text)

    assert len(chunks) > 0


def test_chunks_are_not_empty():
    """
    No chunk should be empty.
    """

    text = "Machine learning is amazing."

    chunks = chunk_text(text)

    assert all(chunk.strip() != "" for chunk in chunks)


def test_chunk_size_limit():
    """
    Chunks should not exceed the specified chunk size.
    """

    text = "A " * 1000

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert all(len(chunk) <= 100 for chunk in chunks)