# ==========================================================
# FILE: rag_pipeline.py
#
# PURPOSE:
# Orchestrate the complete Retrieval-Augmented Generation
# (RAG) workflow.
#
# RESPONSIBILITY:
# 1. Retrieve relevant chunks from ChromaDB.
# 2. Build a structured, source-aware prompt.
# 3. Send the prompt to Ollama.
# 4. Return the generated answer + sources.
#
# CITATION UX CLEANUP:
# - Metadata is still provided to the LLM for grounding.
# - Raw SOURCE/PAGE/CHUNK lines are no longer expected
#   in the final answer.
# - The frontend (Streamlit/FastAPI) is now the single
#   authoritative place where citations are displayed.
# ==========================================================

from app.llm.ollama_client import generate_response
from app.query.query_knowledge_base import query_knowledge_base


def build_context(results: dict) -> str:
    """
    Convert retrieved documents into a structured context string.

    Metadata is preserved for grounding, but formatted in a
    cleaner way so the model focuses on answering rather than
    repeating citations.
    """

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    formatted_chunks = []

    for doc, meta in zip(documents, metadatas):

        file_name = meta.get("file_name", "unknown_file")
        page_number = meta.get("page_number", "unknown_page")

        formatted_chunk = f"""
Document: {file_name}
Page: {page_number}

Content:
{doc}
""".strip()

        formatted_chunks.append(formatted_chunk)

    return "\n\n".join(formatted_chunks)


def build_prompt(question: str, context: str) -> str:
    """
    Construct the RAG prompt.
    """

    return f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
respond exactly with:

"I cannot answer from the provided documents."

Do NOT invent information.

Do NOT mention page numbers, chunk ids, file names,
or source metadata in your final answer.

The user interface will display citations separately.

Provide a concise and well-structured explanation.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()


def ask_rag(question: str) -> dict:
    """
    Execute the complete RAG pipeline.
    """

    results = query_knowledge_base(question)

    context = build_context(results)

    prompt = build_prompt(
        question=question,
        context=context,
    )

    answer = generate_response(prompt)

    metadata = results["metadatas"][0]

    sources = []

    for item in metadata:

        sources.append(
            {
                "file_name": item["file_name"],
                "page_number": item.get("page_number"),
                "chunk_id": item["chunk_id"],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }
