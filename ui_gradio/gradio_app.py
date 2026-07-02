# ==========================================================
# FILE: gradio_app.py
#
# PURPOSE:
# Gradio frontend for Multi-Document RAG system.
#
# RESPONSIBILITY:
# - Upload multiple PDFs
# - Ask questions via FastAPI
# - Display answers and sources
#
# ARCHITECTURE:
#
# User
#   ↓
# Gradio UI
#   ↓
# FastAPI
#   ↓
# RAG Pipeline
#   ↓
# ChromaDB + Ollama
#
# DESIGN:
# - Dark theme
# - Bright blue UI
# - Multi-file upload
#
# NEW IMPROVEMENT:
# - Docker-compatible networking
# - Local execution compatibility
# ==========================================================

import os

import gradio as gr
import requests

# ----------------------------------------------------------
# API endpoints
# ----------------------------------------------------------
FASTAPI_BASE_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000",
)

ASK_URL = f"{FASTAPI_BASE_URL}/ask"

UPLOAD_URL = f"{FASTAPI_BASE_URL}/upload_pdfs"


# ==========================================================
# RAG QUESTION FUNCTION
# ==========================================================
def ask_question(question: str):

    if not question.strip():
        return "Please enter a question.", ""

    try:

        response = requests.post(
            ASK_URL,
            json={"question": question},
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()

        answer = result["answer"]

        sources_text = ""

        for source in result["sources"]:

            sources_text += (
                f"• {source['file_name']} "
                f"(page {source['page_number']}, "
                f"chunk {source['chunk_id']})\n"
            )

        return answer, sources_text

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to FastAPI. " "Make sure the API server is running.",
            "",
        )

    except Exception as error:

        return f"Unexpected error: {error}", ""


# ==========================================================
# PDF UPLOAD FUNCTION (MULTI-FILE)
# ==========================================================
def upload_pdfs(files):

    if not files:
        return "Please upload at least one PDF file."

    try:

        files_payload = []

        for file in files:

            file_path = file.name

            with open(file_path, "rb") as f:

                file_name = os.path.basename(file_path)

                files_payload.append(
                    (
                        "files",
                        (
                            file_name,
                            f.read(),
                            "application/pdf",
                        ),
                    )
                )

        response = requests.post(
            UPLOAD_URL,
            files=files_payload,
            timeout=600,
        )

        response.raise_for_status()

        result = response.json()

        uploaded = "\n".join([f"✓ {f}" for f in result["uploaded_files"]])

        return result["message"] + "\n\n" + uploaded

    except Exception as error:

        return f"Upload failed: {error}"


# ==========================================================
# THEME
# ==========================================================
theme = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
)


# ==========================================================
# GRADIO INTERFACE
# ==========================================================
with gr.Blocks(
    theme=theme,
    title="Multi-Document RAG Engine",
    css="""
    body {
        background-color: #0E1117;
    }

    .gradio-container {
        background-color: #0E1117 !important;
        color: white !important;
    }

    h1, h2, h3 {
        color: #4DA6FF !important;
        font-weight: 700 !important;
    }

    button {
        background-color: #4DA6FF !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        padding: 10px !important;
    }

    button:hover {
        background-color: #2F8CFF !important;
    }

    textarea, input {
        background-color: #1A1F2B !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    """,
) as demo:

    # ------------------------------------------------------
    # TITLE
    # ------------------------------------------------------
    gr.Markdown("""
        # Multi-Document RAG Knowledge Engine

        Ask questions or upload multiple PDF documents.
        """)

    # ------------------------------------------------------
    # UPLOAD SECTION
    # ------------------------------------------------------
    gr.Markdown("## Upload PDFs")

    file_input = gr.File(
        file_count="multiple",
        file_types=[".pdf"],
        label="Select one or more PDF files",
    )

    upload_button = gr.Button("Upload PDFs")

    upload_output = gr.Textbox(
        label="Upload Status",
        lines=5,
    )

    upload_button.click(
        fn=upload_pdfs,
        inputs=file_input,
        outputs=upload_output,
    )

    gr.Markdown("---")

    # ------------------------------------------------------
    # QUESTION SECTION
    # ------------------------------------------------------
    gr.Markdown("## Ask Questions")

    question_box = gr.Textbox(
        label="Enter your question",
        placeholder=("How are machine learning and deep learning related?"),
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer_box = gr.Textbox(
        label="Answer",
        lines=10,
    )

    sources_box = gr.Textbox(
        label="Sources",
        lines=6,
    )

    ask_button.click(
        fn=ask_question,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )


# ==========================================================
# LAUNCH APP
# ==========================================================
if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False,
    )
