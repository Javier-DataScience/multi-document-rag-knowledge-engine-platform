# ==========================================================
# FILE: test_query_knowledge_base.py
#
# PURPOSE:
# Unit tests for the retrieval engine.
#
# RESPONSIBILITY:
# Verify that ChromaDB retrieval returns valid results.
#
# TEST STRATEGY:
# - Ensure a dictionary is returned
# - Ensure documents are retrieved
# - Ensure metadata exists
# - Ensure the number of results respects top_k
#
# ARCHITECTURAL ROLE:
# Retrieval is the heart of the RAG system.
# If retrieval fails, generation cannot be trusted.
# ==========================================================

from app.query.query_knowledge_base import query_knowledge_base


def test_query_returns_dictionary():
    """
    The retrieval engine should return a dictionary.
    """

    results = query_knowledge_base(
        "What is machine learning?",
        top_k=2,
    )

    assert isinstance(results, dict)


def test_query_returns_documents():
    """
    At least one document should be retrieved.
    """

    results = query_knowledge_base(
        "What is deep learning?",
        top_k=2,
    )

    assert len(results["documents"][0]) > 0


def test_query_returns_metadata():
    """
    Retrieved chunks should contain metadata.
    """

    results = query_knowledge_base(
        "What is deep learning?",
        top_k=2,
    )

    assert results["metadatas"][0][0] is not None


def test_query_respects_top_k():
    """
    The number of returned chunks should not exceed top_k.
    """

    top_k = 2

    results = query_knowledge_base(
        "What is machine learning?",
        top_k=top_k,
    )

    assert len(results["documents"][0]) <= top_k