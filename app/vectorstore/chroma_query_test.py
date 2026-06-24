# ==========================================================
# FILE: chroma_query_test.py
#
# PURPOSE:
# Demonstrate how to query documents stored in ChromaDB.
#
# RESPONSIBILITY:
# Connect to an existing collection and retrieve the most
# relevant documents for a query.
#
# INPUTS:
# A natural language query.
#
# OUTPUTS:
# The most relevant stored documents.
#
# ARCHITECTURAL ROLE:
# This validates the retrieval layer before introducing
# PDFs, metadata, FastAPI, Ollama, or user interfaces.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_collection("test_collection")

results = collection.query(
    query_texts=["What is machine learning?"],
    n_results=2
)

print(results)