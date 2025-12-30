import os
import random
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "job_model.pkl")

CATEGORICAL_COLS = [
    "ProgrammingLanguages",
    "Technologies",
    "Specialization",
    "IndustryPreference",
    "LocationPreference"
]

NUMERIC_COLS = [
    "GPA",
    "Projects",
    "Internships",
    "CommunicationSkills",
    "ProblemSolvingSkills",
    "Adaptability"
]

TARGET = "JobRole"


def train():
    os.makedirs(MODEL_DIR, exist_ok=True)

    # ---------------------------
    # Synthetic Dataset Creation
    # ---------------------------
    data = []
    for _ in range(1000):
        data.append({
            "GPA": round(random.uniform(5.5, 9.5), 2),
            "ProgrammingLanguages": "Python, SQL",
            "Technologies": "ML, Pandas",
            "Projects": random.randint(1, 6),
            "Internships": random.randint(0, 2),
            "CommunicationSkills": random.randint(1, 5),
            "ProblemSolvingSkills": random.randint(1, 5),
            "Adaptability": random.randint(1, 5),
            "Specialization": random.choice(["AI", "Data Science", "Web Development"]),
            "IndustryPreference": random.choice(["IT", "Finance", "Healthcare"]),
            "LocationPreference": random.choice(["Remote", "India", "USA"]),
            "JobRole": random.choice([
                "ML Engineer",
                "Data Analyst",
                "Backend Developer",
                "AI Researcher"
            ])
        })

    df = pd.DataFrame(data)

    for col in CATEGORICAL_COLS:
        df[col] = df[col].astype(str)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # ---------------------------
    # Preprocessing
    # ---------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLS)
        ]
    )

    # ---------------------------
    # Random Forest Model
    # ---------------------------
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ))
        ]
    )

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("✅ Random Forest model trained and saved successfully!")


if __name__ == "__main__":
    train()
