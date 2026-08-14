from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from document_loader import split_documents

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = BASE_DIR / "data" / "career_notes"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "mentor"


# --------------------------------------------------
# 2. Load career documents
# --------------------------------------------------

print("Loading career mentor documents...")

loader = DirectoryLoader(
    str(DOCUMENTS_DIR),
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()

print(f"Loaded documents: {len(documents)}")


# --------------------------------------------------
# 3. Split documents into chunks
# --------------------------------------------------

print("Splitting documents into chunks...")

chunks = split_documents(documents)

print(f"Created chunks: {len(chunks)}")


if len(chunks) == 0:
    print("ERROR: No chunks were created.")
    print(f"Check this folder: {DOCUMENTS_DIR}")
    raise SystemExit


# --------------------------------------------------
# 4. Create embeddings
# --------------------------------------------------

print("Creating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 5. Create FAISS vector database
# --------------------------------------------------

print("Creating Career Mentor FAISS index...")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# --------------------------------------------------
# 6. Save vector database
# --------------------------------------------------

VECTORSTORE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

vectorstore.save_local(str(VECTORSTORE_DIR))

print()
print("======================================")
print("Career Mentor index created successfully!")
print("======================================")
print(f"Saved to: {VECTORSTORE_DIR}")
print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")