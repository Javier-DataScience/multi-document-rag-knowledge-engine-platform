# ==========================================================
# FILE: test_rag_pipeline.py
#
# PURPOSE:
# Unit tests for the RAG orchestration layer.
#
# RESPONSIBILITY:
# Verify the behavior of pure functions inside
# rag_pipeline.py.
#
# NOTE:
# We DO NOT test:
# - Ollama
# - ChromaDB
# - End-to-end generation
#
# Those belong to integration tests.
#
# We ONLY test deterministic logic:
# - Context construction
# - Prompt construction
# ==========================================================

from app.llm.rag_pipeline import build_context
from app.llm.rag_pipeline import build_prompt


def test_build_context_combines_documents():
    """
    Multiple retrieved documents should be joined
    into a single context string.
    """

    results = {
        "documents": [
            [
                "Machine learning is a branch of AI.",
                "Deep learning uses neural networks.",
            ]
        ]
    }

    context = build_context(results)

    assert "Machine learning" in context
    assert "Deep learning" in context
    assert "\n\n" in context


def test_build_prompt_contains_context_and_question():
    """
    The generated prompt must include both the
    context and the user question.
    """

    question = "What is deep learning?"
    context = "Deep learning uses neural networks."

    prompt = build_prompt(question, context)

    assert question in prompt
    assert context in prompt
    assert "ANSWER:" in prompt
