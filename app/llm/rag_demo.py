# ==========================================================
# FILE: rag_demo.py
#
# PURPOSE:
# Manually test the complete Retrieval-Augmented Generation
# (RAG) pipeline from end to end.
#
# RESPONSIBILITY:
# 1. Send a user question.
# 2. Retrieve relevant chunks from ChromaDB.
# 3. Generate an answer using Ollama (llama3).
# 4. Display the answer.
# 5. Display the sources used by the model.
#
# INPUTS:
# - A hardcoded question for manual experimentation.
#
# OUTPUTS:
# - Generated answer.
# - Source documents and chunk identifiers.
#
# ARCHITECTURAL ROLE:
# This file is ONLY for manual experimentation and
# debugging during development.
#
# It is NOT part of:
# - Unit testing
# - Integration testing
# - CI/CD pipelines
# - Production code
#
# The purpose of this script is to verify that:
#
# Question
#     ↓
# Retrieval
#     ↓
# Prompt Construction
#     ↓
# Ollama Generation
#     ↓
# Source Attribution
#
# works correctly as a complete RAG workflow.
# ==========================================================

from app.llm.rag_pipeline import ask_rag

# ----------------------------------------------------------
# Example user question.
# ----------------------------------------------------------
question = "How are machine learning and deep learning related?"


# ----------------------------------------------------------
# Execute the complete RAG pipeline.
# The function now returns:
#
# {
#     "answer": "...",
#     "sources": [...]
# }
# ----------------------------------------------------------
result = ask_rag(question)


# ----------------------------------------------------------
# Print the original question.
# ----------------------------------------------------------
print("\nQUESTION:\n")
print(question)


# ----------------------------------------------------------
# Print the generated answer.
# ----------------------------------------------------------
print("\nANSWER:\n")
print(result["answer"])


# ----------------------------------------------------------
# Print the retrieved sources.
# ----------------------------------------------------------
print("\nSOURCES:\n")

for source in result["sources"]:
    print(f"- {source['file_name']} " f"(chunk {source['chunk_id']})")
