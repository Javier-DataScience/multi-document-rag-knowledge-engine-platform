# ==========================================================
# FILE: main.py
#
# PURPOSE:
# Expose the RAG system through a simple FastAPI API.
#
# RESPONSIBILITY:
# - Receive user questions.
# - Execute the RAG pipeline.
# - Return answers and sources as JSON.
#
# ARCHITECTURAL ROLE:
# Thin presentation layer on top of the existing
# RAG system.
#
# DESIGN DECISION:
# Keep the API intentionally simple:
#
# POST /ask
#
# Request:
# {
#     "question": "What is deep learning?"
# }
#
# Response:
# {
#     "answer": "...",
#     "sources": [...]
# }
#
# No authentication.
# No databases.
# No background jobs.
# No enterprise patterns.
# ==========================================================

from fastapi import FastAPI

from app.api.schemas import QuestionRequest, QuestionResponse, Source
from app.llm.rag_pipeline import ask_rag

app = FastAPI(
    title="Multi-Document RAG Knowledge Engine",
    description="Simple educational RAG system using ChromaDB and Ollama.",
    version="1.0.0",
)


@app.get("/")
def health_check() -> dict[str, str]:
    """
    Simple health endpoint.
    """

    return {
        "status": "healthy",
        "service": "multi-document-rag-knowledge-engine",
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    """
    Execute the complete RAG pipeline.
    """

    result = ask_rag(request.question)

    sources = [
        Source(
            file_name=source["file_name"],
            page_number=source["page_number"],
            chunk_id=source["chunk_id"],
        )
        for source in result["sources"]
    ]

    return QuestionResponse(
        answer=result["answer"],
        sources=sources,
    )


# ----------------------------------------------------------
# Local execution
# ----------------------------------------------------------
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
