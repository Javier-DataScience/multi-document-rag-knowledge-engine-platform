# ==========================================================
# FILE: chroma_insert_test.py
#
# PURPOSE:
# Demonstrate how to insert data into a ChromaDB collection.
#
# RESPONSIBILITY:
# Create a collection and store sample text records.
#
# INPUTS:
# None
#
# OUTPUTS:
# - Inserts sample documents into ChromaDB.
# - Stores records persistently on disk.
#
# ARCHITECTURAL ROLE:
# Before loading PDFs and generating embeddings, we learn
# how documents are stored inside ChromaDB collections.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_or_create_collection(
    name="test_collection"
)

collection.add(
    documents=[
        "Machine learning is a branch of artificial intelligence.",
        "Deep learning is a subset of machine learning."
    ],
    ids=[
        "doc_1",
        "doc_2"
    ]
)

print("Documents inserted successfully.")
print(f"Document count: {collection.count()}")