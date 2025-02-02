import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor  # Example model; use your trained model

# Load the pre-trained model and preprocessor (Scaler and ColumnTransformer)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    preprocessor = pickle.load(f)

# Define FastAPI app
app = FastAPI()

# Define feature types
skew_features = ['quota', 'occupiedSlots', 'tuitionFee', 'profCount', 'assoCount', 'docCount', 'revenue', 
                 'totalPreference', 'top1PreferenceRatio', 'avgAdmittedStudentPrefOrder', 'top10AdmittedRatio', 
                 'admittedTotalPref', 'admittedTotalDepartmentPref', 'currentStudentCount', 'totalForeignStudents']

continuous_features = ['academicYear', 'universityName', 'faculty', 'departmentName', 'idOSYM', 'scholarshipRate', 
                       'universityLocation', 'universityRegion', 'topRanking', 'avgAdmissionRanking', 'baseAdmissionRanking', 
                       'stdDeviationStudents', 'outOfCityStudentRate', 'avgOrderofPreference', 'top1AdmittedRatio', 
                       'top3AdmittedRatio', 'baseScore', 'topScore', 'totalStudentNumber', 'Urap_Rank', 'Urap_Score', 
                       'avg_monthly_income_group', 'Time_for_employment', 'employment_rate', 'base_salary_by_year', 
                       'inflation_by_year', 'growth_by_year']

binary_features = [
    'universityType_devlet', 'universityType_vakıf', 'programType_DİL', 'programType_EA', 'programType_SAY', 
    'programType_SÖZ', 'language_Almanca', 'language_Arapça', 'language_Bulgarca', 'language_Ermenice', 
    'language_Fransızca', 'language_Korece', 'language_Lehçe', 'language_Rusça', 'language_Türkçe', 'language_Çince', 
    'language_İngilizce', 'language_İspanyolca', 'language_İtalyanca', 'baseRanking', 'idOSYM_flag'
]

# Define request structure (User input model)
class UserInput(BaseModel):
    university_name: str
    faculty: str
    department: str
    scholarship_rate: float
    language: str
    other_features: list  # This will take numeric & binary features from user input

@app.post("/predict/")
def predict(user_input: UserInput):
    """Preprocess user input and predict based on trained model."""
    
    # Convert input to DataFrame
    user_df = pd.DataFrame([user_input.other_features], columns=continuous_features + binary_features)
    
    # Apply log transformation to skewed features (to handle skewness)
    user_df[skew_features] = user_df[skew_features] + 0.1  # Add small constant to avoid log(0)
    user_df[skew_features] = np.log1p(user_df[skew_features])
    
    # Drop baseRanking from the input
    user_df = user_df.drop(columns=['baseRanking'])
    user_df = user_df.drop(columns=['idOSYM_flag'])
    
    # Apply the saved preprocessor (StandardScaler + other transformations)
    processed_input = preprocessor.transform(user_df)
    
    # Convert back to DataFrame
    processed_df = pd.DataFrame(processed_input, columns=continuous_features + binary_features)
    
    # Make prediction using the loaded model
    prediction = model.predict(processed_df)
    
    # Return prediction result
    return {"prediction": prediction.tolist()}

