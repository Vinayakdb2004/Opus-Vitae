import streamlit as st
from resume_generator import generate_resume
from job_recommender import recommend_job

st.set_page_config(page_title="Opus Vitae", layout="centered")

st.sidebar.title(" Navigation")
page = st.sidebar.radio("Go to", ["Resume Generator", "Job Recommendation"])

# ---------------- RESUME PAGE ----------------
if page == "Resume Generator":
    st.title(" Resume Generator")
    st.caption("Create a professional, ATS-friendly resume")

    name = st.text_input("Full Name", placeholder="Vinayak D B")
    education = st.text_input("Education", placeholder="B.Tech in AI")
    experience = st.number_input("Years of Experience", 0, 20, 2)
    skills = st.text_area("Skills", placeholder="Python, ML, SQL, Deep Learning")
    job_role = st.text_input("Target Job Role", placeholder="Machine Learning Engineer")

    if st.button("Generate Resume"):
        if not all([name, education, skills, job_role]):
            st.warning("⚠ Please fill all fields")
        else:
            path = generate_resume(
                name, skills, experience, education, job_role
            )

            st.success(" Resume generated")
            with open(path, "rb") as f:
                st.download_button(
                    "📥 Download Resume",
                    f,
                    file_name=path.split("/")[-1],
                    mime="application/pdf"
                )

# ---------------- JOB RECOMMENDATION PAGE ----------------
elif page == "Job Recommendation":
    st.title("🤖 Job Recommendation System")
    st.caption("Find the best role based on your skills")

    skills = st.text_input("Skills")
    experience = st.number_input("Experience (years)", min_value=0, max_value=50)
    education = st.selectbox("Education", ["Diploma", "Bachelors", "Masters", "PhD"])


    if st.button("Recommend Job"):
        if not skills:
            st.warning("⚠ Enter at least one skill")
        else:
            job = recommend_job(skills=skills,
                        experience=experience,
                         education=education)
            st.success(f" Recommended Role: **{job}**")
