# ==========================================================
# FILE: pdf_loader.py
#
# PURPOSE:
# Load multiple PDF files and extract raw text from them.
#
# RESPONSIBILITY:
# This module ONLY handles reading PDFs and extracting text.
#
# INPUTS:
# - Path to a PDF file or folder of PDFs
#
# OUTPUTS:
# - Raw extracted text per PDF
#
# ARCHITECTURAL ROLE:
# This is the FIRST stage of the multi-document RAG pipeline.
# It feeds clean text into the chunking module.
#
# NEW IMPROVEMENT:
# Preserve page boundaries so future versions of the RAG
# system can provide page-level citations.
# ==========================================================

from pypdf import PdfReader
import os


def load_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a single PDF file.

    Returns
    -------
    list[dict]
        [
            {
                "page": 1,
                "text": "..."
            },
            {
                "page": 2,
                "text": "..."
            }
        ]
    """

    reader = PdfReader(file_path)

    pages = []

    for page_index, page in enumerate(reader.pages):

        extracted = page.extract_text()

        if extracted:

            pages.append(
                {
                    "page": page_index + 1,
                    "text": extracted,
                }
            )

    return pages


def load_all_pdfs(folder_path: str) -> dict:
    """
    Load all PDFs inside a folder.

    Returns
    -------
    dict
        key   = file name
        value = list of pages

        Example:

        {
            "book.pdf": [
                {"page": 1, "text": "..."},
                {"page": 2, "text": "..."},
            ]
        }
    """

    pdf_texts = {}

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            full_path = os.path.join(folder_path, file)

            pdf_texts[file] = load_pdf(full_path)

    return pdf_texts
