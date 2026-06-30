# ==========================================================
# FILE: query_knowledge_base.py
#
# PURPOSE:
# Query ChromaDB knowledge base with simple document balancing.
#
# FIXES:
# - removes circular imports
# - stabilizes retrieval output
# - ensures correct metadata handling
# - passes MyPy validation
# ==========================================================

from typing import Any

import chromadb


def query_knowledge_base(
    question: str,
    top_k: int = 3,
    max_chunks_per_document: int = 2,
) -> dict[str, Any]:
    """
    Retrieve relevant chunks from ChromaDB with simple balancing.
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_collection(name="knowledge_base")

    # ------------------------------------------------------
    # Retrieve more candidates than needed
    # ------------------------------------------------------
    raw_results = collection.query(
        query_texts=[question],
        n_results=10,
    )

    if (
        raw_results["documents"] is None
        or raw_results["metadatas"] is None
        or raw_results["distances"] is None
    ):
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
        }

    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]
    distances = raw_results["distances"][0]

    # ------------------------------------------------------
    # Balance documents (avoid dominance of single PDF)
    # ------------------------------------------------------
    document_counter: dict[str, int] = {}

    selected_documents: list[str] = []
    selected_metadatas: list[dict[str, Any]] = []
    selected_distances: list[float] = []

    for doc, meta, dist in zip(documents, metadatas, distances):

        file_name = str(meta.get("file_name", "unknown"))

        count = document_counter.get(file_name, 0)

        if count >= max_chunks_per_document:
            continue

        selected_documents.append(doc)
        selected_metadatas.append(dict(meta))
        selected_distances.append(dist)

        document_counter[file_name] = count + 1

        if len(selected_documents) >= top_k:
            break

    return {
        "documents": [selected_documents],
        "metadatas": [selected_metadatas],
        "distances": [selected_distances],
    }


# ----------------------------------------------------------
# Manual test
# ----------------------------------------------------------
if __name__ == "__main__":

    question = "Explain the relationship between machine learning and deep learning."

    results = query_knowledge_base(
        question,
        top_k=3,
        max_chunks_per_document=2,
    )

    print("\nQUESTION:\n")
    print(question)

    print("\nTOP RESULTS:\n")

    for i in range(len(results["documents"][0])):

        print("\n----------------------------------")

        print(f"FILE: {results['metadatas'][0][i].get('file_name')}")

        print(f"PAGE: {results['metadatas'][0][i].get('page_number')}")

        print(f"CHUNK: {results['metadatas'][0][i].get('chunk_id')}")

        print(f"DISTANCE: {results['distances'][0][i]:.4f}")

        print("\nTEXT:\n")

        print(results["documents"][0][i])
