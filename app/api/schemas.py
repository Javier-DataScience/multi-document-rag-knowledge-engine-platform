# ==========================================================
# FILE: schemas.py
#
# PURPOSE:
# Pydantic schemas for FastAPI.
# ==========================================================

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    file_name: str
    page_number: int | None = None
    chunk_id: int


class QuestionResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]


class UploadResponse(BaseModel):
    message: str
    uploaded_files: list[str]
