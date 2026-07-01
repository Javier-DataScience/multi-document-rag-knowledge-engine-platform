# ==========================================================
# FILE: streamlit_app.py
#
# PURPOSE:
# Streamlit frontend for the Multi-Document RAG system.
#
# RESPONSIBILITY:
# - Upload multiple PDF documents.
# - Ask questions through FastAPI.
# - Display answers and citations.
#
# ARCHITECTURAL ROLE:
#
# User
#   ↓
# Streamlit UI
#   ↓
# FastAPI
#   ↓
# RAG Pipeline
#   ↓
# ChromaDB + Ollama
#
# DESIGN PRINCIPLES:
# - Dark theme
# - Bright text
# - Large buttons
# - Educational project
# - FastAPI as intermediary layer
# ==========================================================

import requests
import streamlit as st

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------
ASK_API_URL = "http://127.0.0.1:8000/ask"

UPLOAD_API_URL = "http://127.0.0.1:8000/upload_pdfs"


# ----------------------------------------------------------
# Page configuration
# ----------------------------------------------------------
st.set_page_config(
    page_title="Multi-Document RAG Engine",
    page_icon="📚",
    layout="wide",
)


# ----------------------------------------------------------
# Custom styling
# ----------------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    h1 {
        color: #4DA6FF;
        font-weight: 700;
    }

    h2, h3 {
        color: #7DB8FF;
    }

    .source-box {
        background-color: #1A1F2B;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #4DA6FF;
    }

    .stButton > button {
        width: 100%;
        background-color: #4DA6FF;
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 12px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #2F8CFF;
        color: #FFFFFF;
    }

    .stButton > button:focus {
        color: #FFFFFF;
        border: none;
        box-shadow: none;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------
# Title
# ----------------------------------------------------------
st.title("Multi-Document RAG Knowledge Engine")

st.write("""
Ask questions about the documents stored in the knowledge base.

The interface communicates with FastAPI, which acts as an
intermediary layer between the frontend and the RAG system.
""")


# ==========================================================
# MULTI-PDF UPLOAD
# ==========================================================
st.header("Upload Documents")

uploaded_files = st.file_uploader(
    "Select one or more PDF files:",
    type=["pdf"],
    accept_multiple_files=True,
)


if st.button(
    "Upload PDFs",
    use_container_width=True,
):

    if not uploaded_files:

        st.warning("Please select at least one PDF file.")

    else:

        try:

            files_payload = []

            for uploaded_file in uploaded_files:

                files_payload.append(
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        ),
                    )
                )

            response = requests.post(
                UPLOAD_API_URL,
                files=files_payload,
                timeout=600,
            )

            response.raise_for_status()

            result = response.json()

            st.success(result["message"])

            st.write("Uploaded files:")

            for file_name in result["uploaded_files"]:

                st.write(f"✓ {file_name}")

        except Exception as error:

            st.error(f"Upload failed: {error}")


st.divider()


# ==========================================================
# QUESTION ANSWERING
# ==========================================================
st.header("Ask Questions")

question = st.text_input(
    "Enter your question:",
    placeholder=("How are machine learning and " "deep learning related?"),
)


if st.button(
    "Ask",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    ASK_API_URL,
                    json={"question": question},
                    timeout=300,
                )

                response.raise_for_status()

                result = response.json()

                # ------------------------------------------
                # Answer
                # ------------------------------------------
                st.subheader("Answer")

                st.write(result["answer"])

                # ------------------------------------------
                # Sources
                # ------------------------------------------
                st.subheader("Sources")

                for source in result["sources"]:

                    st.markdown(
                        f"""
                        <div class="source-box">
                            <b>{source["file_name"]}</b><br>
                            Page: {source["page_number"]}<br>
                            Chunk: {source["chunk_id"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure the API server is running."
                )

            except Exception as error:

                st.error(f"Unexpected error: {error}")
