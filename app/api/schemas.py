# ==========================================================
# FILE: schemas.py
#
# PURPOSE:
# Define all API request and response models.
#
# RESPONSIBILITY:
# - Validate incoming requests.
# - Standardize outgoing responses.
#
# ARCHITECTURAL ROLE:
# This module acts as the contract between clients
# and the FastAPI application.
#
# DESIGN DECISION:
# Keep the API intentionally simple:
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
# ==========================================================

from pydantic import BaseModel


class Source(BaseModel):
    """
    Metadata describing a retrieved chunk.
    """

    file_name: str
    page_number: int
    chunk_id: int


class QuestionRequest(BaseModel):
    """
    User question sent to the RAG system.
    """

    question: str


class QuestionResponse(BaseModel):
    """
    Final answer returned by the RAG system.
    """

    answer: str
    sources: list[Source]
