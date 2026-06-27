# ==========================================================
# FILE: ollama_client.py
#
# PURPOSE:
# Provide a minimal wrapper around the local Ollama server.
#
# RESPONSIBILITY:
# This module ONLY sends prompts to a local LLM and
# returns the generated response.
#
# INPUTS:
# - prompt (str)
# - model name
#
# OUTPUTS:
# - generated text (str)
#
# ARCHITECTURAL ROLE:
# This is the first layer of the generation system.
# Retrieval logic must NOT live here.
# Prompt engineering must NOT live here.
# RAG orchestration must NOT live here.
# ==========================================================

import ollama


def generate_response(
    prompt: str,
    model: str = "llama3",
) -> str:
    """
    Send a prompt to Ollama and return the generated text.
    """

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]
