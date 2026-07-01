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
# NEW IMPROVEMENTS:
# - Absolute imports for package compatibility.
# - ingest_single_pdf() for FastAPI uploads.
# - Duplicate chunk protection.
# - Compatible with Docker and future Compose setup.
# ==========================================================

from pathlib import Path

import chromadb

from app.ingestion.chunker import chunk_text
from app.ingestion.pdf_loader import load_all_pdfs


# ----------------------------------------------------------
# Shared helper
# ----------------------------------------------------------
def _insert_pdf_into_collection(
    collection,
    file_name: str,
    pages: list,
) -> int:
    """
    Insert a single PDF into ChromaDB.

    Returns:
        Number of chunks inserted.
    """

    inserted_chunks = 0
    global_chunk_index = 0

    print(f"\nProcessing: {file_name}")

    for page_data in pages:

        page_number = page_data["page"]
        page_text = page_data["text"]

        chunks = chunk_text(page_text)

        print(f"Page {page_number}: " f"{len(chunks)} chunks generated")

        for chunk in chunks:

            chunk_id = f"{file_name}_chunk_{global_chunk_index}"

            # ----------------------------------------------
            # Avoid duplicate insertions
            # ----------------------------------------------
            try:

                existing = collection.get(ids=[chunk_id])

                if existing["ids"]:
                    global_chunk_index += 1
                    continue

            except Exception:
                pass

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

            inserted_chunks += 1
            global_chunk_index += 1

    return inserted_chunks


# ----------------------------------------------------------
# Multi-document ingestion
# ----------------------------------------------------------
def ingest_pdfs(pdf_folder: str = "./data") -> None:
    """
    Load every PDF inside a folder and insert them into
    ChromaDB.
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_or_create_collection(name="knowledge_base")

    pdfs = load_all_pdfs(pdf_folder)

    total_chunks = 0

    for file_name, pages in pdfs.items():

        inserted = _insert_pdf_into_collection(
            collection=collection,
            file_name=file_name,
            pages=pages,
        )

        total_chunks += inserted

    print("\n===================================")
    print(f"New chunks inserted: {total_chunks}")
    print(f"Collection size: {collection.count()}")
    print("===================================")


# ----------------------------------------------------------
# Single-document ingestion
# ----------------------------------------------------------
def ingest_single_pdf(file_path: str) -> None:
    """
    Ingest exactly one PDF.

    Intended for FastAPI upload workflows.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_or_create_collection(name="knowledge_base")

    pdfs = load_all_pdfs(str(pdf_path.parent))

    file_name = pdf_path.name

    if file_name not in pdfs:
        raise ValueError(f"Could not load {file_name}")

    inserted = _insert_pdf_into_collection(
        collection=collection,
        file_name=file_name,
        pages=pdfs[file_name],
    )

    print("\n===================================")
    print(f"Uploaded file: {file_name}")
    print(f"New chunks inserted: {inserted}")
    print(f"Collection size: {collection.count()}")
    print("===================================")


# ----------------------------------------------------------
# Manual execution
# ----------------------------------------------------------
if __name__ == "__main__":

    ingest_pdfs()
