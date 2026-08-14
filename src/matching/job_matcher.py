import pandas as pd
import re


def normalize_text(text):
    """
    Convert text into lowercase so that
    Python, PYTHON and python are treated
    as the same word.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    return text


def get_job_skills(skills_text):
    """
    Convert the skills column from the dataset
    into a list of individual skills.
    """

    if not isinstance(skills_text, str):
        return []

    skills = skills_text.split(";")

    skills = [
        skill.strip().lower()
        for skill in skills
        if skill.strip()
    ]

    return skills


def find_matching_skills(resume_text, job_skills):

    resume_text = normalize_text(resume_text)

    matched = []
    missing = []

    for skill in job_skills:

        # Escape special characters
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):

            matched.append(skill)

        else:

            missing.append(skill)

    return matched, missing


def calculate_match_percentage(
    matched_skills,
    total_skills
):

    if total_skills == 0:
        return 0

    percentage = (
        len(matched_skills)
        / total_skills
    ) * 100

    return round(percentage, 2)


def match_resume_with_jobs(
    resume_text,
    jobs
):

    results = []

    for _, job in jobs.iterrows():

        job_skills = get_job_skills(
            job["skills"]
        )

        matched, missing = find_matching_skills(
            resume_text,
            job_skills
        )

        match_percentage = calculate_match_percentage(
            matched,
            len(job_skills)
        )

        results.append({
            "job_id": job["job_id"],
            "job_title": job["job_title"],
            "company": job["company"],
            "location": job["location"],
            "match_percentage": match_percentage,
            "matched_skills": matched,
            "missing_skills": missing
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="match_percentage",
        ascending=False
    )

    return results_df