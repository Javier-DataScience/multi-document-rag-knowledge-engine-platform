# ==========================================================
# FILE: gradio_app.py
#
# PURPOSE:
# Gradio frontend for the Multi-Document RAG system.
#
# RESPONSIBILITY:
# - Collect user questions.
# - Send requests to FastAPI.
# - Display answers and sources.
#
# ARCHITECTURAL ROLE:
#
# User
#   ↓
# Gradio UI
#   ↓
# FastAPI (/ask)
#   ↓
# RAG Pipeline
#   ↓
# ChromaDB + Ollama
#
# DESIGN PRINCIPLES:
# - Dark theme
# - Bright blue accents
# - White text
# - Minimal interface
# - Educational project
# ==========================================================

import requests
import gradio as gr

FASTAPI_URL = "http://127.0.0.1:8000/ask"


def ask_question(question: str):

    if not question.strip():
        return "Please enter a question.", ""

    try:

        response = requests.post(
            FASTAPI_URL,
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


# ----------------------------------------------------------
# Theme
# ----------------------------------------------------------
theme = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
)


# ----------------------------------------------------------
# Interface
# ----------------------------------------------------------
with gr.Blocks(
    theme=theme,
    title="Multi-Document RAG Knowledge Engine",
    css="""
    body {
        background-color: #0E1117;
    }

    .gradio-container {
        background-color: #0E1117 !important;
        color: white !important;
    }

    button {
        background-color: #4DA6FF !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
    }

    button:hover {
        background-color: #2F8CFF !important;
    }
    """,
) as demo:

    gr.Markdown("""
    <h1 style="
        color:#4DA6FF;
        font-weight:700;
        margin-bottom:20px;
    ">
        Multi-Document RAG Knowledge Engine
    </h1>

    <p style="
        color:white;
        font-size:16px;
    ">
        Ask questions about the documents stored in the
        knowledge base.

        The interface communicates with FastAPI, which acts
        as an intermediary layer between the frontend and
        the RAG system.
    </p>
    """)

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


if __name__ == "__main__":

    demo.launch(
        inbrowser=True,
        share=False,
    )
