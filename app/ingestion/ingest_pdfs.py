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
#
# NEW IMPROVEMENT:
# Store page_number metadata to enable future
# page-level citations.
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

    collection = client.get_or_create_collection(name="knowledge_base")

    # ------------------------------------------------------
    # Load all PDFs
    # ------------------------------------------------------
    pdfs = load_all_pdfs(pdf_folder)

    total_chunks = 0

    # ------------------------------------------------------
    # Process every PDF
    # ------------------------------------------------------
    for file_name, pages in pdfs.items():

        print(f"\nProcessing: {file_name}")

        global_chunk_index = 0

        # --------------------------------------------------
        # Process every page independently
        # --------------------------------------------------
        for page_data in pages:

            page_number = page_data["page"]
            page_text = page_data["text"]

            chunks = chunk_text(page_text)

            print(f"Page {page_number}: " f"{len(chunks)} chunks generated")

            # ----------------------------------------------
            # Insert chunks
            # ----------------------------------------------
            for chunk in chunks:

                chunk_id = f"{file_name}_chunk_{global_chunk_index}"

                collection.add(
                    documents=[chunk],
                    ids=[chunk_id],
                    metadatas=[
                        {
                            "file_name": file_name,
                            "chunk_id": global_chunk_index,
                            "page_number": page_number,
                        }
                    ],
                )

                total_chunks += 1
                global_chunk_index += 1

    print("\n===================================")
    print(f"Total chunks inserted: {total_chunks}")
    print(f"Collection size: {collection.count()}")
    print("===================================")


if __name__ == "__main__":
    ingest_pdfs()
