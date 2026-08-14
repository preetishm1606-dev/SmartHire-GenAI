from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embedding(text):

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding