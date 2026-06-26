# ==========================================================
# FILE: test_pdf_loader.py
#
# PURPOSE:
# Unit tests for the PDF loading module.
#
# RESPONSIBILITY:
# Verify that PDFs are discovered and their text is
# correctly extracted.
#
# TEST STRATEGY:
# - Ensure a dictionary is returned
# - Ensure PDFs are detected
# - Ensure extracted text is not empty
# - Ensure filenames end with .pdf
#
# ARCHITECTURAL ROLE:
# PDF loading is the entry point of the entire RAG
# pipeline. If ingestion fails, everything fails.
# ==========================================================

from app.ingestion.pdf_loader import load_all_pdfs


PDF_FOLDER = "./data"


def test_loader_returns_dictionary():
    """
    The loader should return a dictionary.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert isinstance(pdfs, dict)


def test_loader_finds_pdfs():
    """
    At least one PDF should be found.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert len(pdfs) > 0


def test_extracted_text_is_not_empty():
    """
    Extracted PDF text should not be empty.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert all(text.strip() != "" for text in pdfs.values())


def test_all_files_are_pdfs():
    """
    All discovered files should end with .pdf.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert all(
        filename.endswith(".pdf")
        for filename in pdfs.keys()
    )