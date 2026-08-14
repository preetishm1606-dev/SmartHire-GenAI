import sys
from pathlib import Path

import faiss
import pandas as pd


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================
# IMPORT EMBEDDING MODEL
# ==========================================

from src.search.embed import model


# ==========================================
# FILE PATHS
# ==========================================

INDEX_PATH = (
    PROJECT_ROOT
    / "vectorstore"
    / "jobs.index"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "vectorstore"
    / "jobs_metadata.csv"
)


# ==========================================
# LOAD FAISS INDEX
# ==========================================

index = faiss.read_index(
    str(INDEX_PATH)
)


# ==========================================
# LOAD JOB INFORMATION
# ==========================================

jobs = pd.read_csv(
    METADATA_PATH
)


# ==========================================
# SEMANTIC JOB SEARCH
# ==========================================

def search_jobs(
    candidate_text,
    top_n=5
):

    # Create candidate embedding
    candidate_embedding = model.encode(
        [candidate_text],
        convert_to_numpy=True
    )

    # Convert to float32
    candidate_embedding = (
        candidate_embedding.astype("float32")
    )

    # Normalize
    faiss.normalize_L2(
        candidate_embedding
    )

    # Search FAISS
    scores, indices = index.search(
        candidate_embedding,
        top_n
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx == -1:
            continue

        job = jobs.iloc[idx]

        results.append({
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "company": job["company"],
            "location": job["location"],
            "skills": job["skills"],
            "description": job["description"],
            "experience": job["experience"],
            "education": job["education"],
            "similarity_score": round(
                float(score) * 100,
                2
            )
        })

    return results