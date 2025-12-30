import pandas as pd
import random

random.seed(42)

PROGRAMMING_LANGUAGES = [
    "Python", "Java", "C++", "JavaScript", "Go", "R"
]

TECHNOLOGIES = [
    "Machine Learning", "Web Development", "Cloud", "Data Science",
    "Cybersecurity", "DevOps", "Mobile Development"
]

SPECIALIZATIONS = [
    "Computer Science", "Software Engineering",
    "AI & ML", "Data Science", "Cyber Security"
]

SOFT_SKILLS = ["Poor", "Average", "Good", "Excellent"]
ADAPTABILITY = ["Low", "Medium", "High"]
INDUSTRIES = ["FinTech", "HealthTech", "EdTech", "E-commerce", "AI Startup"]
LOCATIONS = ["Remote", "Hybrid", "Onsite"]

JOB_ROLES = [
    "Software Developer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Cloud Engineer",
    "Cybersecurity Analyst",
    "DevOps Engineer"
]

data = []

for _ in range(1000):
    record = {
        "ProgrammingLanguages": random.choice(PROGRAMMING_LANGUAGES),
        "Technologies": random.choice(TECHNOLOGIES),
        "Specialization": random.choice(SPECIALIZATIONS),
        "GPA": round(random.uniform(2.5, 4.0), 2),
        "Projects": random.randint(1, 6),
        "Internships": random.randint(0, 3),
        "CommunicationSkills": random.choice(SOFT_SKILLS),
        "ProblemSolvingSkills": random.choice(SOFT_SKILLS),
        "Adaptability": random.choice(ADAPTABILITY),
        "IndustryPreference": random.choice(INDUSTRIES),
        "LocationPreference": random.choice(LOCATIONS),
        "JobRole": random.choice(JOB_ROLES)
    }
    data.append(record)

df = pd.DataFrame(data)
df.to_csv("job_role_dataset.csv", index=False)

print("Synthetic dataset generated: job_role_dataset.csv")
