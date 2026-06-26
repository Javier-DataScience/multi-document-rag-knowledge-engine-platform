# ==========================================================
# FILE: test_chunker.py
#
# PURPOSE:
# Validate chunking logic on sample text.
# ==========================================================

from chunker import chunk_text

sample_text = """
Machine learning is a branch of artificial intelligence.
It focuses on learning patterns from data.

Deep learning is a subset of machine learning.
It uses neural networks with many layers.
"""

chunks = chunk_text(sample_text, chunk_size=50, overlap=10)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i+1}:")
    print(chunk)