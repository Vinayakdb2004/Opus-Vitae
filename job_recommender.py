import joblib
import pandas as pd

MODEL_PATH = "job_model.pkl"

def recommend_job(skills, experience, education):
    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([{
        "skills": skills,
        "experience": experience,
        "education": education
    }])

    prediction = model.predict(input_df)
    return prediction[0]
