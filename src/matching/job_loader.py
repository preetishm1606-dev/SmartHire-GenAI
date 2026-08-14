import pandas as pd

JOB_FILE = "data/jobs/jobs.csv"


def load_jobs():
    jobs = pd.read_csv(JOB_FILE)

    print("Number of jobs:", len(jobs))
    print("Columns:")
    print(jobs.columns.tolist())

    return jobs


if __name__ == "__main__":
    jobs = load_jobs()

    print("\nFirst 5 jobs:")
    print(jobs.head())