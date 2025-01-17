import streamlit as st
import pandas as pd
import joblib
from fpdf import FPDF
from io import BytesIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load and prepare the dataset for job role recommendation
file_path = r"D:\OneDrive\Desktop\python_based_last_project prototype\job_role_dataset.csv"

try:
    df = pd.read_csv(file_path, sep=',')  # Adjust `sep` as necessary
    #st.write("Dataset loaded successfully!")
except FileNotFoundError:
    st.error(f"Error: File not found at {file_path}. Ensure the file exists.")
    exit()
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
    exit()

# Expected features and target
expected_columns = ['ProgrammingLanguages', 'Technologies', 'Specialization',
                    'GPA', 'Projects', 'Internships', 'CommunicationSkills',
                    'ProblemSolvingSkills', 'Adaptability', 'IndustryPreference',
                    'RolePreference', 'LocationPreference', 'JobRole']

# Check for missing columns
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    st.error(f"Error: Missing columns in the dataset: {missing_columns}")
    exit()

# Check for columns containing lists and convert them to strings if necessary
list_columns = ['ProgrammingLanguages', 'Technologies']
for col in list_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Use pd.get_dummies for one-hot encoding
encoded_df = pd.get_dummies(df)

# Define features (X) and target variable (y)
features = expected_columns[:-1]  # All columns except 'JobRole'
target = 'JobRole'

X = df[features]
y = df[target]

# Encode categorical features using one-hot encoding
X = pd.get_dummies(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)
#st.write("Model trained successfully!")

# Make predictions on the test set
y_pred = rf_classifier.predict(X_test)

# Evaluate model performance


# Load the trained Random Forest model
job_model = rf_classifier

# Styled PDF generation class
class StyledResumePDF(FPDF):
    def __init__(self, name, contact, email):
        super().__init__()
        self.name = name
        self.contact = contact
        self.email = email
        self.set_font('Arial', size=12)

    def header(self):
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', size=20)
        self.cell(200, 15, txt=self.name, ln=True, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', size=12)
        self.cell(200, 10, txt=f"Contact: {self.contact} | Email: {self.email}", ln=True, align='C')
        self.ln(10)

    def add_section(self, title, items, bullet=True):
        self.set_fill_color(230, 230, 230)
        self.set_font('Arial', 'B', size=14)
        self.cell(200, 10, txt=title, ln=True, align='L', fill=True)
        self.ln(2)
        self.set_font('Arial', size=12)
        for item in items:
            if bullet:
                self.cell(10, 10, txt="*", ln=False)
                self.cell(190, 10, txt=item, ln=True)
            else:
                self.cell(200, 10, txt=f"- {item}", ln=True)
        self.ln(5)
        self.set_fill_color(0, 102, 204)
        self.cell(200, 0, ln=True, border='T', fill=True)
        self.ln(5)

def generate_pdf(data):
    pdf = StyledResumePDF(name=data['name'], contact=data['contact'], email=data['email'])
    pdf.add_page()
    pdf.add_section("Education", data['education'])
    pdf.add_section("Experience", data['experience'])
    pdf.add_section("Skills", data['skills'], bullet=False)
    pdf.add_section("Projects", data['projects'])
    pdf.add_section("Certifications", data['certifications'])
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def input_list(label):
    st.write(f"Enter {label} (One per line):")
    items = st.text_area(f"{label} (One item per line)", "")
    return [item.strip() for item in items.split("\n") if item.strip()]

def main():
    st.title("Resume Builder with Job Recommendation")
    st.sidebar.title("Navigation")
    menu = ["Build Resume", "Job Recommendation"]
    choice = st.sidebar.radio("Go to", menu)

    if choice == "Build Resume":
        st.header("Build Your Resume")

        # User Input for Resume
        name = st.text_input("Full Name")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email Address")

        st.write("### Add Details")
        education = input_list("Education Details (Degree, Institution, Year)")
        experience = input_list("Experience Details (Job Title, Company, Years)")
        skills = input_list("Skills")
        projects = input_list("Projects (Title, Description)")
        certifications = input_list("Certifications (Name, Issuing Organization, Year)")

        if st.button("Generate Resume"):
            if not all([name, contact, email]):
                st.error("Please fill out all required fields!")
            else:
                data = {
                    "name": name,
                    "contact": contact,
                    "email": email,
                    "education": education,
                    "experience": experience,
                    "skills": skills,
                    "projects": projects,
                    "certifications": certifications,
                }
                pdf_buffer = generate_pdf(data)
                st.download_button(
                    label="Download Resume PDF",
                    data=pdf_buffer,
                    file_name="styled_resume.pdf",
                    mime="application/pdf",
                )

    elif choice == "Job Recommendation":
        st.header("Job Recommendation System")
        st.write("Enter your skill ratings to get a recommended job role.")

        # User Input for Job Recommendation
        user_skills = {}
        skill_columns = ['ProgrammingLanguages', 'Technologies', 'Specialization', 'GPA', 'Projects', 'Internships', 
                         'CommunicationSkills', 'ProblemSolvingSkills', 'Adaptability', 'IndustryPreference', 
                         'RolePreference', 'LocationPreference']
                         
        for skill in skill_columns:
            user_skills[skill] = st.text_input(f"Enter {skill} (comma separated)")

        # Convert input into DataFrame for prediction
        user_input_df = pd.DataFrame([user_skills])

        # Ensure the input matches training data format
        user_input_df = pd.get_dummies(user_input_df)
        missing_cols = set(X.columns) - set(user_input_df.columns)
        for col in missing_cols:
            user_input_df[col] = 0  # Add missing columns with default value 0
        user_input_df = user_input_df[X.columns]  # Reorder columns to match training data

        # Make prediction for job role
        if st.button("Get Job Recommendation"):
            predicted_job_role = job_model.predict(user_input_df)
            st.success(f"Recommended Job Role: **{predicted_job_role[0]}**")

if __name__ == "__main__":
    main()
