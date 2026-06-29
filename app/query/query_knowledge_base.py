# ==========================================================
# FILE: query_knowledge_base.py
#
# PURPOSE:
# Query the multi-document knowledge base stored in ChromaDB.
#
# RESPONSIBILITY:
# - Connect to the persistent vector database
# - Retrieve the most relevant chunks
# - Apply basic document balancing
# - Display associated metadata
#
# INPUTS:
# - User question
#
# OUTPUTS:
# - Top matching chunks and metadata
#
# ARCHITECTURAL ROLE:
# This module is the retrieval layer of the RAG system.
# It intentionally performs NO text generation.
#
# DESIGN DECISION:
# Retrieval must be fully validated before introducing
# more advanced RAG techniques.
#
# NEW IMPROVEMENT:
# Limit the number of chunks retrieved from a single
# document so one PDF cannot dominate the results.
# ==========================================================

import chromadb


def query_knowledge_base(
    question: str,
    top_k: int = 3,
    max_chunks_per_document: int = 2,
):
    """
    Retrieve the most relevant chunks from ChromaDB.

    Parameters
    ----------
    question : str
        User question.

    top_k : int
        Final number of chunks returned.

    max_chunks_per_document : int
        Maximum number of chunks allowed from a single PDF.
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_collection(name="knowledge_base")

    # ------------------------------------------------------
    # Retrieve more candidates than we actually need.
    # This gives us room to perform document balancing.
    # ------------------------------------------------------
    raw_results = collection.query(
        query_texts=[question],
        n_results=10,
    )

    documents = raw_results["documents"][0]
    metadatas = raw_results["metadatas"][0]
    distances = raw_results["distances"][0]

    # ------------------------------------------------------
    # Keep track of how many chunks have been selected
    # from each document.
    # ------------------------------------------------------
    document_counter = {}

    selected_documents = []
    selected_metadatas = []
    selected_distances = []

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):

        file_name = metadata["file_name"]

        current_count = document_counter.get(file_name, 0)

        # --------------------------------------------------
        # Skip documents that already reached the limit.
        # --------------------------------------------------
        if current_count >= max_chunks_per_document:
            continue

        selected_documents.append(doc)
        selected_metadatas.append(metadata)
        selected_distances.append(distance)

        document_counter[file_name] = current_count + 1

        # --------------------------------------------------
        # Stop once we have enough final chunks.
        # --------------------------------------------------
        if len(selected_documents) >= top_k:
            break

    return {
        "documents": [selected_documents],
        "metadatas": [selected_metadatas],
        "distances": [selected_distances],
    }


if __name__ == "__main__":

    question = "Explain the relationship between machine learning and deep learning."

    results = query_knowledge_base(
        question,
        top_k=4,
        max_chunks_per_document=2,
    )

    print("\nQUESTION:")
    print(question)

    print("\nTOP RESULTS:")

    for i in range(len(results["documents"][0])):

        print("\n----------------------------------")

        print(f"FILE: " f"{results['metadatas'][0][i]['file_name']}")

        print(f"CHUNK: " f"{results['metadatas'][0][i]['chunk_id']}")

        print(f"DISTANCE: " f"{results['distances'][0][i]:.4f}")

        print("\nTEXT:")

        print(results["documents"][0][i])
