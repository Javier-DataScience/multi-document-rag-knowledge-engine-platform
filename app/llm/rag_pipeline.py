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
# IMPROVEMENT (Phase D step 1):
# Context now includes:
# - file name
# - page number
# - chunk id
# ==========================================================

from app.query.query_knowledge_base import query_knowledge_base
from app.llm.ollama_client import generate_response


def build_context(results: dict) -> str:
    """
    Convert retrieved documents into a structured context string.
    Now includes document metadata for better grounding.
    """

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    formatted_chunks = []

    for doc, meta in zip(documents, metadatas):

        file_name = meta.get("file_name", "unknown_file")
        page_number = meta.get("page_number", "unknown_page")
        chunk_id = meta.get("chunk_id", "unknown_chunk")

        formatted_chunk = f"""
=== SOURCE DOCUMENT: {file_name} | PAGE: {page_number} | CHUNK: {chunk_id} ===

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
If the answer is not contained in the context,
say: "I cannot answer from the provided documents."

Use the sources to justify your answer.

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

    prompt = build_prompt(question, context)

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