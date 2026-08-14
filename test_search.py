from src.search.job_search import search_jobs


candidate = """
BCA student with skills in Python, SQL,
Excel, Pandas and data analysis.
Interested in Data Analyst and
Machine Learning roles.
"""


results = search_jobs(
    candidate,
    top_n=5
)


print("\n🎯 TOP MATCHING JOBS\n")


for position, job in enumerate(
    results,
    start=1
):

    print(
        f"{position}. "
        f"{job['job_title']} "
        f"— {job['similarity_score']}%"
    )

    print(
        f"   Company: {job['company']}"
    )

    print(
        f"   Location: {job['location']}"
    )

    print()