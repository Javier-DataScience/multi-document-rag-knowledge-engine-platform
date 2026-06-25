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
# ==========================================================

from pypdf import PdfReader
import os


def load_pdf(file_path: str) -> str:
    """
    Extract text from a single PDF file.
    """
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def load_all_pdfs(folder_path: str) -> dict:
    """
    Load all PDFs inside a folder.

    Returns:
        dict:
            key = file name
            value = extracted text
    """
    pdf_texts = {}

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            pdf_texts[file] = load_pdf(full_path)

    return pdf_texts