from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


# ==========================================
# CAREER NOTES FOLDER
# ==========================================

CAREER_NOTES_PATH = (
    PROJECT_ROOT
    / "data"
    / "career_notes"
)


# ==========================================
# LOAD CAREER NOTES
# ==========================================

def load_career_notes():

    documents = []

    for file_path in CAREER_NOTES_PATH.glob("*.md"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name
            }
        )

        documents.append(document)

    return documents


# ==========================================
# SPLIT DOCUMENTS
# ==========================================

def split_documents(documents):

    text_splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks