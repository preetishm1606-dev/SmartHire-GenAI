from src.mentor.document_loader import (
    load_career_notes,
    split_documents
)


# ==========================================
# LOAD CAREER NOTES
# ==========================================

documents = load_career_notes()

print(
    f"Loaded documents: {len(documents)}"
)


# ==========================================
# SPLIT DOCUMENTS INTO CHUNKS
# ==========================================

chunks = split_documents(
    documents
)

print(
    f"Created chunks: {len(chunks)}"
)


# ==========================================
# DISPLAY FIRST FEW CHUNKS
# ==========================================

for number, chunk in enumerate(
    chunks[:5],
    start=1
):

    print(
        "\n" + "=" * 50
    )

    print(
        f"CHUNK {number}"
    )

    print(
        f"Source: "
        f"{chunk.metadata['source']}"
    )

    print(
        chunk.page_content[:500]
    )