import sys
from pathlib import Path

import faiss
import pandas as pd
import numpy as np

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.search.embed import model


# ==========================================
# PATHS
# ==========================================

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "jobs"
    / "jobs.csv"
)

VECTORSTORE_PATH = (
    PROJECT_ROOT
    / "vectorstore"
)


# ==========================================
# LOAD DATASET
# ==========================================

jobs = pd.read_csv(DATASET_PATH)

print(
    f"Loaded {len(jobs)} jobs."
)


# ==========================================
# CREATE TEXT FOR EACH JOB
# ==========================================

job_texts = []

for _, job in jobs.iterrows():

    text = f"""
Job Title: {job['job_title']}

Company: {job['company']}

Location: {job['location']}

Skills: {job['skills']}

Description: {job['description']}

Experience: {job['experience']}

Education: {job['education']}
"""

    job_texts.append(text)


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

print("Creating job embeddings...")

embeddings = model.encode(
    job_texts,
    convert_to_numpy=True
)


# ==========================================
# NORMALIZE EMBEDDINGS
# ==========================================

embeddings = embeddings.astype(
    "float32"
)

faiss.normalize_L2(
    embeddings
)


# ==========================================
# CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(
    dimension
)

index.add(embeddings)


# ==========================================
# SAVE INDEX
# ==========================================

VECTORSTORE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

index_path = (
    VECTORSTORE_PATH
    / "jobs.index"
)

faiss.write_index(
    index,
    str(index_path)
)


# ==========================================
# SAVE JOB DATA
# ==========================================

jobs_path = (
    VECTORSTORE_PATH
    / "jobs_metadata.csv"
)

jobs.to_csv(
    jobs_path,
    index=False
)


print("✅ FAISS index created successfully!")

print(
    f"Index saved to: {index_path}"
)

print(
    f"Metadata saved to: {jobs_path}"
)