import os

from dotenv import load_dotenv

from google import genai

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# Load Career Mentor FAISS database
# --------------------------------------------------

VECTORSTORE_PATH = "vectorstore/mentor"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# Career Mentor function
# --------------------------------------------------

def ask_career_mentor(question):

    # Retrieve relevant career information
    results = vectorstore.similarity_search(
        question,
        k=3
    )

    # Combine retrieved information
    context_parts = []

    for document in results:

        source = document.metadata.get(
            "source",
            "Career notes"
        )

        content = document.page_content

        context_parts.append(
            f"Source: {source}\n{content}"
        )

    context = "\n\n".join(context_parts)


    # --------------------------------------------------
    # Prompt Gemini
    # --------------------------------------------------

    prompt = f"""
You are SmartHire Career Mentor.

Answer the user's career question using the
career information provided below.

Career information:
--------------------
{context}
--------------------

User question:
{question}

Instructions:
1. Give a clear and useful answer.
2. Use the provided career information.
3. Do not invent information that is not supported
   by the provided context.
4. Give practical next steps when appropriate.
5. Keep the answer easy for a student to understand.
"""


    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text