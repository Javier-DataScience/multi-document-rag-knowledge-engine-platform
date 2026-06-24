# ==========================================================
# FILE: chroma_test.py
#
# PURPOSE:
# Demonstrate the basic creation of a persistent ChromaDB
# collection and verify that the vector database can store
# data on disk.
#
# RESPONSIBILITY:
# This module is only responsible for creating and accessing
# a ChromaDB collection.
#
# INPUTS:
# None
#
# OUTPUTS:
# - Creates a persistent ChromaDB database folder.
# - Creates a collection named "test_collection".
# - Prints confirmation messages.
#
# ARCHITECTURAL ROLE:
# Phase B introduces ChromaDB as the replacement for FAISS.
# This file validates that the vector database layer works
# before introducing documents, embeddings, retrieval,
# FastAPI, or user interfaces.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_or_create_collection(
    name="test_collection"
)

print("Collection created successfully.")
print(f"Collection name: {collection.name}")