# ==========================================================
# FILE: query_knowledge_base.py
#
# PURPOSE:
# Query the multi-document knowledge base stored in ChromaDB.
#
# RESPONSIBILITY:
# - Connect to the persistent vector database
# - Retrieve the most relevant chunks
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
# Ollama or any LLM component.
# ==========================================================

import chromadb


def query_knowledge_base(question: str, top_k: int = 3):
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    client = chromadb.PersistentClient(path="./data/chroma_db")

    collection = client.get_collection(name="knowledge_base")

    results = collection.query(query_texts=[question], n_results=top_k)

    return results


if __name__ == "__main__":

    question = "Explain the relationship between machine learning and deep learning."

    results = query_knowledge_base(question)

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
