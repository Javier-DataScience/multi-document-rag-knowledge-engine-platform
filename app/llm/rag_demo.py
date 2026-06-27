# ==========================================================
# FILE: rag_demo.py
#
# PURPOSE:
# Manually test the complete RAG pipeline.
#
# RESPONSIBILITY:
# Send a question through retrieval and generation.
#
# ARCHITECTURAL ROLE:
# Manual experimentation only.
# Not part of automated tests.
# ==========================================================

from app.llm.rag_pipeline import ask_rag

question = "What is deep learning?"

answer = ask_rag(question)

print("\nQUESTION:\n")
print(question)

print("\nANSWER:\n")
print(answer)
