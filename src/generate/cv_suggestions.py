from src.generation.gemini_client import client

from src.generate.prompts import (
    CV_IMPROVEMENT_PROMPT
)


def generate_cv_suggestions(
    resume_text,
    job
):

    prompt = CV_IMPROVEMENT_PROMPT.format(
        job_title=job["job_title"],
        job_skills=job["skills"],
        job_description=job["description"],
        resume_text=resume_text
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text