# ==========================================================
# FILE: chroma_filter_test.py
#
# PURPOSE:
# Demonstrate metadata-based filtering in ChromaDB queries.
#
# RESPONSIBILITY:
# Retrieve documents only from a specific source file
# using metadata filters.
#
# INPUTS:
# A query + metadata filter (file_name)
#
# OUTPUTS:
# Filtered retrieval results from a specific document.
#
# ARCHITECTURAL ROLE:
# This is a core feature for multi-document RAG systems,
# allowing retrieval to be constrained to a single PDF.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_collection("metadata_collection")

results = collection.query(
    query_texts=["What is deep learning?"],
    n_results=2,
    where={"file_name": "deep_learning_book.pdf"},
)

print(results)
