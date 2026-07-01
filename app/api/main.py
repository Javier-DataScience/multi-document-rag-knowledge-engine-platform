# ==========================================================
# FILE: main.py
#
# PURPOSE:
# FastAPI entrypoint for the Multi-Document
# RAG Knowledge Engine.
#
# RESPONSIBILITY:
# - Receive user questions
# - Execute the RAG pipeline
# - Upload multiple PDFs
# - Trigger ingestion
#
# NOTE:
# Swagger UI may render multiple-file uploads as
# array<string>, but Streamlit and Gradio will
# correctly support true multiple-file selection.
# ==========================================================

from pathlib import Path
import shutil
from typing import Annotated

from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from app.api.schemas import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse,
)

from app.ingestion.ingest_pdfs import ingest_single_pdf
from app.llm.rag_pipeline import ask_rag

# ----------------------------------------------------------
# FastAPI application
# ----------------------------------------------------------
app = FastAPI(
    title="Multi-Document RAG Knowledge Engine",
    version="1.1.0",
)


# ----------------------------------------------------------
# Root endpoint
# ----------------------------------------------------------
@app.get("/")
def root():

    return {"message": "Multi-Document RAG API is running."}


# ----------------------------------------------------------
# Ask endpoint
# ----------------------------------------------------------
@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask(request: QuestionRequest):

    return ask_rag(request.question)


# ----------------------------------------------------------
# Upload multiple PDFs
# ----------------------------------------------------------
@app.post(
    "/upload_pdfs",
    response_model=UploadResponse,
)
def upload_pdfs(
    files: Annotated[
        list[UploadFile],
        File(
            ...,
            description="One or more PDF files.",
        ),
    ],
):

    data_folder = Path("./data")
    data_folder.mkdir(exist_ok=True)

    uploaded_files: list[str] = []

    try:

        for file in files:

            if file.filename is None:

                continue

            if not file.filename.lower().endswith(".pdf"):

                raise HTTPException(
                    status_code=400,
                    detail=(f"{file.filename} is not a PDF file."),
                )

            destination = data_folder / file.filename

            with destination.open("wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

            ingest_single_pdf(str(destination))

            uploaded_files.append(file.filename)

        return {
            "message": ("PDF files uploaded and " "ingested successfully."),
            "uploaded_files": uploaded_files,
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
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
