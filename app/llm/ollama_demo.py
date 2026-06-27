# ==========================================================
# FILE: ollama_demo.py
#
# PURPOSE:
# Manually verify that the local Ollama model works.
#
# RESPONSIBILITY:
# Send a simple prompt and print the response.
#
# ARCHITECTURAL ROLE:
# Manual experimentation only.
# This file is NOT part of automated testing.
# ==========================================================

from app.llm.ollama_client import generate_response

response = generate_response("Explain machine learning in three sentences.")

print("\nMODEL RESPONSE:\n")
print(response)
