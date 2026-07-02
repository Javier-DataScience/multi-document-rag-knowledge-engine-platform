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
#
# LOCAL MODE:
# - Uses localhost:11434
#
# DOCKER MODE:
# - Uses host.docker.internal:11434
#
# DESIGN PRINCIPLE:
# Automatically support both execution environments so
# this problem never reappears.
# ==========================================================

import os

import ollama

# ----------------------------------------------------------
# Ollama host configuration
# ----------------------------------------------------------
#
# If running inside Docker, docker-compose sets:
#
#     OLLAMA_HOST=http://host.docker.internal:11434
#
# Otherwise, local execution falls back to:
#
#     http://localhost:11434
#
# ----------------------------------------------------------
OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

OLLAMA_CLIENT = ollama.Client(host=OLLAMA_HOST)


def generate_response(
    prompt: str,
    model: str = "llama3",
) -> str:
    """
    Send a prompt to Ollama and return the generated text.
    """

    response = OLLAMA_CLIENT.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # ------------------------------------------------------
    # Ollama returns values typed as Any.
    # We explicitly convert the generated content to str
    # so MyPy can verify the function contract.
    # ------------------------------------------------------
    return str(response["message"]["content"])
