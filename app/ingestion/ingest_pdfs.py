# ==========================================================
# FILE: ingest_pdfs.py
#
# PURPOSE:
# Coordinate the complete ingestion pipeline for multiple
# PDF documents.
#
# RESPONSIBILITY:
# - Load PDFs
# - Chunk document text
# - Generate metadata
# - Store chunks inside ChromaDB
#
# INPUTS:
# - Folder containing PDF files
#
# OUTPUTS:
# - Persistent vector database entries
#
# ARCHITECTURAL ROLE:
# This module is the bridge between document ingestion
# and the retrieval engine.
#
# DESIGN DECISION:
# All documents are stored inside ONE collection:
#     knowledge_base
#
# Metadata is used to distinguish sources.
# ==========================================================

import chromadb

from pdf_loader import load_all_pdfs
from chunker import chunk_text


def ingest_pdfs(pdf_folder: str = "./data"):
    """
    Load all PDFs, chunk them, and store them in ChromaDB.
    """

    # ------------------------------------------------------
    # Create persistent client
    # ------------------------------------------------------
    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_or_create_collection(
        name="knowledge_base"
    )

    # ------------------------------------------------------
    # Load all PDFs
    # ------------------------------------------------------
    pdfs = load_all_pdfs(pdf_folder)

    total_chunks = 0

    # ------------------------------------------------------
    # Process every PDF
    # ------------------------------------------------------
    for file_name, text in pdfs.items():

        print(f"\nProcessing: {file_name}")

        chunks = chunk_text(text)

        print(f"Chunks generated: {len(chunks)}")

        # --------------------------------------------------
        # Insert chunks
        # --------------------------------------------------
        for index, chunk in enumerate(chunks):

            chunk_id = f"{file_name}_chunk_{index}"

            collection.add(
                documents=[chunk],
                ids=[chunk_id],
                metadatas=[
                    {
                        "file_name": file_name,
                        "chunk_id": index
                    }
                ]
            )

            total_chunks += 1

    print("\n===================================")
    print(f"Total chunks inserted: {total_chunks}")
    print(f"Collection size: {collection.count()}")
    print("===================================")


if __name__ == "__main__":
    ingest_pdfs()