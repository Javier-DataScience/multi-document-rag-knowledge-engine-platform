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
# - Ensure pages are returned as lists
# - Ensure extracted page text is not empty
# - Ensure filenames end with .pdf
#
# ARCHITECTURAL ROLE:
# PDF loading is the entry point of the entire RAG
# pipeline. If ingestion fails, everything fails.
#
# NEW IMPROVEMENT:
# The loader now preserves page boundaries and returns:
#
# {
#     "document.pdf": [
#         {"page": 1, "text": "..."},
#         {"page": 2, "text": "..."},
#     ]
# }
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


def test_loader_returns_page_lists():
    """
    Every document should return a list of pages.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert all(isinstance(pages, list) for pages in pdfs.values())


def test_extracted_page_text_is_not_empty():
    """
    Every extracted page should contain non-empty text.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    for pages in pdfs.values():

        for page in pages:

            assert page["text"].strip() != ""


def test_all_files_are_pdfs():
    """
    All discovered files should end with .pdf.
    """

    pdfs = load_all_pdfs(PDF_FOLDER)

    assert all(filename.endswith(".pdf") for filename in pdfs.keys())
