# ==========================================================
# FILE: rag_pipeline.py
#
# PURPOSE:
# Orchestrate the complete Retrieval-Augmented Generation
# (RAG) workflow.
#
# RESPONSIBILITY:
# 1. Retrieve relevant chunks from ChromaDB.
# 2. Build a prompt using those chunks.
# 3. Send the prompt to Ollama.
# 4. Return the generated answer.
#
# INPUTS:
# - User question (str)
#
# OUTPUTS:
# - Generated answer (str)
#
# ARCHITECTURAL ROLE:
# This module connects retrieval and generation while
# keeping both systems independent.
#
# NEW IMPROVEMENT:
# Source metadata now includes page numbers to enable
# page-level citations in future UI and API layers.
# ==========================================================

from app.query.query_knowledge_base import query_knowledge_base
from app.llm.ollama_client import generate_response


def build_context(results: dict) -> str:
    """
    Convert retrieved documents into a single context string.
    """

    documents = results["documents"][0]

    return "\n\n".join(documents)


def build_prompt(question: str, context: str) -> str:
    """
    Construct the RAG prompt.
    """

    return f"""
You are a helpful assistant.

Answer ONLY using the provided context.
If the answer is not contained in the context,
say: "I cannot answer from the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


def ask_rag(question: str) -> dict:
    """
    Execute the complete RAG pipeline.
    """

    # ------------------------------------------------------
    # Retrieve relevant chunks
    # ------------------------------------------------------
    results = query_knowledge_base(question)

    # ------------------------------------------------------
    # Build context for the LLM
    # ------------------------------------------------------
    context = build_context(results)

    # ------------------------------------------------------
    # Build the final prompt
    # ------------------------------------------------------
    prompt = build_prompt(question, context)

    # ------------------------------------------------------
    # Generate the answer using Ollama
    # ------------------------------------------------------
    answer = generate_response(prompt)

    # ------------------------------------------------------
    # Extract source metadata
    # ------------------------------------------------------
    metadata = results["metadatas"][0]

    sources = []

    for item in metadata:

        sources.append(
            {
                "file_name": item["file_name"],
                "page_number": item["page_number"],
                "chunk_id": item["chunk_id"],
            }
        )

    # ------------------------------------------------------
    # Return both answer and sources
    # ------------------------------------------------------
    return {
        "answer": answer,
        "sources": sources,
    }
