# ==========================================================
# FILE: test_pdf_loader.py
#
# PURPOSE:
# Validate PDF ingestion works for multiple files.
# ==========================================================

from pdf_loader import load_all_pdfs

print("Starting ingestion test...")

pdfs = load_all_pdfs("./data")

print(f"PDFs found: {len(pdfs)}")

for name, text in pdfs.items():
    print(f"\nFILE: {name}")
    print(f"TEXT PREVIEW: {text[:200]}")