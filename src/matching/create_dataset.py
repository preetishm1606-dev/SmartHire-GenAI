import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "jobs"

OCCUPATION_FILE = DATA_DIR / "occupation_data.csv"
SOFTWARE_FILE = DATA_DIR / "software_skills.csv"

OUTPUT_FILE = DATA_DIR / "jobs.csv"


# --------------------------------------------------
# 2. Read O*NET files
# --------------------------------------------------

print("Reading occupation data...")

occupations = pd.read_csv(
    OCCUPATION_FILE,
    encoding="utf-8"
)

print("Reading software skills data...")

software = pd.read_csv(
    SOFTWARE_FILE,
    encoding="utf-8"
)


# --------------------------------------------------
# 3. Display column names
# --------------------------------------------------

print("\nOccupation columns:")
print(occupations.columns.tolist())

print("\nSoftware skill columns:")
print(software.columns.tolist())


# --------------------------------------------------
# 4. Rename important columns
# --------------------------------------------------

occupations = occupations.rename(
    columns={
        "O*NET-SOC Code": "job_id",
        "Title": "job_title",
        "Description": "description"
    }
)

software = software.rename(
    columns={
        "O*NET-SOC Code": "job_id",
        "Workplace Example": "technology",
        "In Demand": "in_demand",
        "Hot Technology": "hot_technology"
    }
)


# --------------------------------------------------
# 5. Combine technologies for each occupation
# --------------------------------------------------

software["technology"] = software["technology"].fillna("")

technology_data = (
    software
    .groupby("job_id")["technology"]
    .apply(
        lambda x: "; ".join(
            sorted(
                set(
                    value.strip()
                    for value in x
                    if value.strip()
                )
            )
        )
    )
    .reset_index()
)


# --------------------------------------------------
# 6. Combine occupation + technology information
# --------------------------------------------------

jobs = occupations[
    ["job_id", "job_title", "description"]
].merge(
    technology_data,
    on="job_id",
    how="left"
)


# --------------------------------------------------
# 7. Rename technology column to skills
# --------------------------------------------------

jobs = jobs.rename(
    columns={
        "technology": "skills"
    }
)


# --------------------------------------------------
# 8. Remove empty values
# --------------------------------------------------

jobs["skills"] = jobs["skills"].fillna("")


# --------------------------------------------------
# 9. Add a source column
# --------------------------------------------------

jobs["source"] = "O*NET 30.3 Database"


# --------------------------------------------------
# 10. Save SmartHire dataset
# --------------------------------------------------

jobs.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# --------------------------------------------------
# 11. Show result
# --------------------------------------------------

print("\n====================================")
print("SmartHire dataset created!")
print("====================================")

print(f"Number of occupations: {len(jobs)}")

print(f"Saved to: {OUTPUT_FILE}")

print("\nColumns:")
print(jobs.columns.tolist())

print("\nFirst 5 records:")
print(jobs.head())