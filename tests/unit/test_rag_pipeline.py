# ==========================================================
# FILE: test_rag_pipeline.py
#
# PURPOSE:
# Unit tests for the RAG pipeline.
# ==========================================================

from app.llm.rag_pipeline import build_context, build_prompt


def test_build_context_combines_documents():
    """
    Multiple retrieved documents should be joined
    into a single structured context string.
    """

    results = {
        "documents": [
            [
                "Machine learning is a branch of AI.",
                "Deep learning uses neural networks.",
            ]
        ],
        "metadatas": [
            [
                {
                    "file_name": "ml_book.pdf",
                    "page_number": 1,
                    "chunk_id": 0,
                },
                {
                    "file_name": "deep_learning.pdf",
                    "page_number": 2,
                    "chunk_id": 1,
                },
            ]
        ],
    }

    context = build_context(results)

    assert "Machine learning is a branch of AI." in context
    assert "Deep learning uses neural networks." in context

    assert "Document: ml_book.pdf" in context
    assert "Document: deep_learning.pdf" in context

    assert "Page: 1" in context
    assert "Page: 2" in context


def test_build_prompt_contains_question_and_context():
    """
    The final prompt should include both
    the user question and retrieved context.
    """

    question = "What is machine learning?"

    context = "Machine learning is a branch of AI."

    prompt = build_prompt(
        question=question,
        context=context,
    )

    assert question in prompt
    assert context in prompt

    assert "ANSWER:" in prompt
