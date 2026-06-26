# ==========================================================
# FILE: chunker.py
#
# PURPOSE:
# Split long raw PDF text into smaller semantic chunks
# for vector embedding and retrieval.
#
# RESPONSIBILITY:
# - Receive raw text
# - Split into manageable chunks
# - Maintain overlap for context preservation
#
# INPUTS:
# - Raw text extracted from PDFs
#
# OUTPUTS:
# - List of text chunks
#
# ARCHITECTURAL ROLE:
# This is the core transformation step between ingestion
# and vector storage in a RAG system.
# ==========================================================


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Split text into overlapping chunks.

    Args:
        text (str): Full document text
        chunk_size (int): Maximum characters per chunk
        overlap (int): Overlap between chunks for context continuity

    Returns:
        list[str]: List of text chunks
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks