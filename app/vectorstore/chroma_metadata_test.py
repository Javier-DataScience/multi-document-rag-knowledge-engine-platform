# ==========================================================
# FILE: chroma_metadata_test.py
#
# PURPOSE:
# Demonstrate how metadata can be stored alongside
# documents inside a ChromaDB collection.
#
# RESPONSIBILITY:
# Store documents together with metadata and retrieve
# them later.
#
# INPUTS:
# Sample documents and metadata.
#
# OUTPUTS:
# Documents stored with metadata.
#
# ARCHITECTURAL ROLE:
# Metadata is the foundation of Phase B because it allows
# multiple PDFs to coexist in the same vector database
# while preserving source information.
# ==========================================================

import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_or_create_collection(
    name="metadata_collection"
)

collection.add(
    documents=[
        "Supervised learning uses labeled data.",
        "Neural networks are commonly used in deep learning."
    ],
    ids=[
        "chunk_1",
        "chunk_2"
    ],
    metadatas=[
        {
            "file_name": "ml_book.pdf",
            "page": 5
        },
        {
            "file_name": "deep_learning_book.pdf",
            "page": 12
        }
    ]
)

print("Documents inserted successfully.")
print(f"Document count: {collection.count()}")