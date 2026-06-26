# ==========================================================
# FILE: chunker.py
#
# PURPOSE:
# Split long documents into semantic chunks suitable for
# vector embeddings and RAG retrieval.
#
# RESPONSIBILITY:
# - Preserve paragraphs and sentences when possible
# - Maintain overlap between chunks
# - Avoid breaking words in the middle
#
# INPUTS:
# - Raw text extracted from PDFs
#
# OUTPUTS:
# - List of semantic text chunks
#
# ARCHITECTURAL ROLE:
# This module forms the core transformation layer between
# PDF ingestion and ChromaDB storage.
#
# DESIGN DECISION:
# We use LangChain's RecursiveCharacterTextSplitter
# because it is a production-standard chunking strategy
# for RAG systems.
# ==========================================================

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
):
    """
    Split text into semantic chunks.

    Args:
        text:
            Raw document text.

        chunk_size:
            Maximum number of characters per chunk.

        chunk_overlap:
            Number of overlapping characters between chunks.

    Returns:
        List[str]:
            Semantic text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    return splitter.split_text(text)