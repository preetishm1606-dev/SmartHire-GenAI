from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Location of Career Mentor vector database
VECTORSTORE_PATH = "vectorstore/mentor"


print("Loading Career Mentor knowledge base...")

# Load the same embedding model used to create the index
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS database
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

print("Career Mentor knowledge base loaded successfully!")


# Ask a test question
question = "What skills should I learn to become a Data Analyst?"

print()
print("Question:")
print(question)

print()
print("Searching Career Mentor knowledge base...")

results = vectorstore.similarity_search(
    question,
    k=3
)


print()
print("========== RESULTS ==========")

for number, document in enumerate(results, start=1):

    print()
    print(f"Result {number}")
    print("----------------------------")

    print("Source:")
    print(document.metadata.get("source", "Unknown"))

    print()
    print("Content:")
    print(document.page_content[:1000])

print()
print("========== SEARCH COMPLETE ==========")