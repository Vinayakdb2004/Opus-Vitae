from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Path to the dataset
file_path = r"D:/Resume_builder_Streamlit/job_role_dataset.csv"

# Load the dataset
try:
    df = pd.read_csv(file_path, sep=',')  # Adjust `sep` as necessary
    #print("Dataset loaded successfully!")
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Ensure the file exists.")
    exit()
except Exception as e:
    print(f"An error occurred while loading the dataset: {e}")
    exit()

# Debugging: Print the column names in the dataset
#print("Columns in the dataset:", df.columns.tolist())

# Expected features and target
expected_columns = ['ProgrammingLanguages', 'Technologies', 'Specialization',
                    'GPA', 'Projects', 'Internships', 'CommunicationSkills',
                    'ProblemSolvingSkills', 'Adaptability', 'IndustryPreference',
                    'RolePreference', 'LocationPreference', 'JobRole']

# Check for missing columns
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in the dataset: {missing_columns}")
    print("Ensure your dataset contains all the required columns.")
    exit()

# Check for columns containing lists and convert them to strings if necessary
list_columns = ['ProgrammingLanguages', 'Technologies']
for col in list_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Use pd.get_dummies for one-hot encoding
encoded_df = pd.get_dummies(df)
#print("Encoding successful!")

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
#print("Model trained successfully!")

# Make predictions on the test set
y_pred = rf_classifier.predict(X_test)
# Define new student data for prediction
new_student_data = {
    'ProgrammingLanguages': 'Python, Java',
    'Technologies': 'Cloud Computing, Machine Learning',
    'Specialization': 'Software Engineering',
    'GPA': 3.8,
    'Projects': 2,
    'Internships': 1,
    'CommunicationSkills': 'Excellent',
    'ProblemSolvingSkills': 'Good',
    'Adaptability': 'High',
    'IndustryPreference': 'FinTech',
    'RolePreference': 'Software Developer',
    'LocationPreference': 'Remote'
}

# Convert new data to a DataFrame
new_student_df = pd.DataFrame([new_student_data])

# Ensure consistent columns with the training data
new_student_df = pd.get_dummies(new_student_df)
missing_cols = set(X.columns) - set(new_student_df.columns)
for col in missing_cols:
    new_student_df[col] = 0  # Add missing columns with default value 0
new_student_df = new_student_df[X.columns]  # Reorder columns to match training data

# Make prediction for the new student
predicted_job_role = rf_classifier.predict(new_student_df)
print(f"Predicted Job Role: {predicted_job_role[0]}")
'''print("    \n \n     ")
accuracy = accuracy_score(y_test, y_pred)
st.write(f"Model Accuracy: {accuracy}")
st.write("Classification Report:")
st.text(classification_report(y_test, y_pred))'''