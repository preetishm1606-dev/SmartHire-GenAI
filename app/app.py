import sys
from pathlib import Path

# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================
# IMPORTS
# ==========================================

import os
import tempfile

import pandas as pd
import streamlit as st

from src.parsing.resume_parser import extract_pdf_text
from src.generation.gemini_client import analyze_resume
from src.search.job_search import search_jobs
from src.generate.cv_suggestions import generate_cv_suggestions
from src.mentor.mentor_rag import ask_career_mentor


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SmartHire GenAI",
    page_icon="💼",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("💼 SmartHire GenAI")

st.subheader(
    "AI-Powered Resume Matching & Career Assistant"
)

st.write(
    "Upload your resume to analyze your profile, "
    "find semantically matching jobs, and improve "
    "your CV for a selected role."
)


# ==========================================
# LOAD JOB DATASET
# ==========================================

st.header("📊 Job Dataset")

try:

    jobs = pd.read_csv(
        PROJECT_ROOT
        / "data"
        / "jobs"
        / "jobs.csv"
    )

    st.success(
        f"Job dataset loaded successfully! "
        f"{len(jobs)} jobs available."
    )

except Exception as e:

    st.error(
        "Could not load the job dataset."
    )

    st.error(str(e))

    st.stop()


# ==========================================
# OPTIONAL DATASET VIEW
# ==========================================

with st.expander("📋 View Job Dataset"):

    st.dataframe(
        jobs,
        width="stretch"
    )


# ==========================================
# RESUME UPLOAD
# ==========================================

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)


# ==========================================
# RESUME PROCESSING
# ==========================================

if uploaded_file is not None:

    st.success(
        f"Resume uploaded successfully: "
        f"{uploaded_file.name}"
    )

    temp_path = None

    try:

        # ----------------------------------
        # Save uploaded PDF temporarily
        # ----------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue()
            )

            temp_path = temp_file.name


        # ----------------------------------
        # Extract resume text
        # ----------------------------------

        resume_text = extract_pdf_text(
            temp_path
        )


        # ----------------------------------
        # Delete temporary file
        # ----------------------------------

        os.remove(temp_path)

        temp_path = None


    except Exception as e:

        if temp_path is not None:

            try:
                os.remove(temp_path)
            except Exception:
                pass


        st.error(
            "Something went wrong while "
            "processing your resume."
        )

        st.error(str(e))

        st.stop()


    # ======================================
    # EXTRACTED RESUME TEXT
    # ======================================

    st.header("📄 Extracted Resume Text")

    if not resume_text.strip():

        st.warning(
            "No readable text was found "
            "in this PDF."
        )

        st.stop()


    st.success(
        "Resume text extracted successfully!"
    )

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Content",
            resume_text,
            height=350
        )


    # ======================================
    # GEMINI RESUME ANALYSIS
    # ======================================

    st.divider()

    st.header("🤖 AI Resume Analysis")

    if st.button(
        "Analyze My Resume",
        key="analyze_resume"
    ):

        with st.spinner(
            "Gemini is analyzing your resume..."
        ):

            try:

                analysis = analyze_resume(
                    resume_text
                )

                st.success(
                    "Resume analysis completed!"
                )

                st.markdown(analysis)


            except Exception as e:

                st.error(
                    "Gemini resume analysis failed."
                )

                st.error(str(e))


    # ======================================
    # SEMANTIC JOB SEARCH
    # ======================================

    st.divider()

    st.header("🔎 Semantic Job Search")

    st.write(
        "Find jobs based on the meaning of your "
        "resume using embeddings and FAISS."
    )


    if st.button(
        "Find Matching Jobs",
        key="find_jobs"
    ):

        with st.spinner(
            "Searching for relevant jobs..."
        ):

            try:

                results = search_jobs(
                    resume_text,
                    top_n=5
                )


                if not results:

                    st.info(
                        "No matching jobs were found."
                    )


                else:

                    st.success(
                        f"Found {len(results)} "
                        "matching jobs!"
                    )


                    # Store results in session
                    st.session_state[
                        "job_results"
                    ] = results


            except Exception as e:

                st.error(
                    "Semantic job search failed."
                )

                st.error(str(e))


    # ======================================
    # DISPLAY JOB RESULTS
    # ======================================

    if "job_results" in st.session_state:

        results = st.session_state[
            "job_results"
        ]


        st.subheader(
            "🎯 Top Matching Jobs"
        )


        for position, job in enumerate(
            results,
            start=1
        ):

            st.subheader(
                f"#{position} 💼 "
                f"{job['job_title']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Company:** "
                    f"{job['company']}"
                )

                st.write(
                    f"**Location:** "
                    f"{job['location']}"
                )

            with col2:

                st.metric(
                    "Semantic Match",
                    f"{job['similarity_score']}%"
                )


            st.write(
                f"**Required Skills:** "
                f"{job['skills']}"
            )

            st.write(
                f"**Description:** "
                f"{job['description']}"
            )

            st.divider()


        # ==================================
        # SELECT TARGET JOB
        # ==================================

        st.header(
            "🎯 Choose a Target Job"
        )

        job_options = [
            (
                f"{job['job_title']} "
                f"— {job['similarity_score']}%"
            )
            for job in results
        ]


        selected_option = st.selectbox(
            "Select the job you want "
            "to improve your CV for:",
            job_options
        )


        selected_index = job_options.index(
            selected_option
        )

        selected_job = results[
            selected_index
        ]


        # ==================================
        # SHOW SELECTED JOB
        # ==================================

        st.info(
            f"Selected role: "
            f"{selected_job['job_title']}"
        )


        # ==================================
        # CV IMPROVEMENT
        # ==================================

        st.header(
            "📝 CV Improvement Generator"
        )

        st.write(
            "Get AI-generated suggestions "
            "for improving your resume "
            "for the selected role."
        )


        if st.button(
            "✨ Generate CV Improvements",
            key="generate_cv"
        ):

            with st.spinner(
                "Gemini is analyzing your CV "
                "against the selected job..."
            ):

                try:

                    suggestions = (
                        generate_cv_suggestions(
                            resume_text,
                            selected_job
                        )
                    )


                    st.success(
                        "CV improvement report "
                        "generated successfully!"
                    )


                    st.markdown(
                        suggestions
                    )


                except Exception as e:

                    st.error(
                        "CV improvement generation "
                        "failed."
                    )

                    st.error(str(e))


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "SmartHire GenAI | "
    "Resume Matching & AI Career Mentor"
)

# ============================================================
# CAREER MENTOR
# ============================================================

st.divider()

st.header("🎓 Career Mentor")

st.write(
    "Ask our AI Career Mentor questions about skills, careers, "
    "learning paths, and job roles."
)

mentor_question = st.text_area(
    "💬 Ask your career question",
    placeholder="Example: What skills should I learn to become a Data Analyst?",
    height=120
)

if st.button("🚀 Ask Career Mentor"):

    if mentor_question.strip():

        with st.spinner("🤖 Career Mentor is thinking..."):

            try:
                mentor_answer = ask_career_mentor(mentor_question)

                st.success("Career Mentor Answer")

                st.write(mentor_answer)

            except Exception as e:

                st.error("Something went wrong while generating the answer.")

                st.code(str(e))

    else:

        st.warning("Please enter a question first.")