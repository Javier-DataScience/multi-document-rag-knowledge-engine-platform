# ==========================================================
# FILE: chroma_metadata_query_test.py
#
# PURPOSE:
# Verify that metadata stored in ChromaDB can be retrieved
# together with relevant documents.
#
# RESPONSIBILITY:
# Query a collection and inspect returned metadata.
#
# INPUTS:
# Natural language query.
#
# OUTPUTS:
# Relevant documents and their metadata.
#
# ARCHITECTURAL ROLE:
# This validates source attribution, which is essential
# for multi-document RAG systems.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_collection("metadata_collection")

results = collection.query(query_texts=["What is supervised learning?"], n_results=2)

print(results)
