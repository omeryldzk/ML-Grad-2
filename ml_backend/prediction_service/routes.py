import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor  # Example model; use your trained model
from database import skew_features, continuous_features, binary_features ,query_bigquery
from models import UserInput

# Load the pre-trained model and preprocessor (Scaler and ColumnTransformer)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    preprocessor = pickle.load(f)

# Define FastAPI app
app = FastAPI()



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

@app.get("/universities/")
def list_universities():
    """Returns a list of available universities."""
    query = "SELECT DISTINCT universityName FROM `bitescout-445308.big_data.university`"
    return query_bigquery(query)


@app.get("/faculties/{university_name}")
def list_faculties(university_name: str):
    """Returns a list of available faculties from the selected university."""
    query = f"""
        SELECT DISTINCT faculty
        FROM `bitescout-445308.big_data.university`
        WHERE universityName = '{university_name}'
    """
    return query_bigquery(query)


@app.get("/departments/{university_name}/{faculty}")
def list_departments(university_name: str, faculty: str):
    """Returns a list of available departments from the selected faculty and university."""
    query = f"""
        SELECT DISTINCT departmentName
        FROM `bitescout-445308.big_data.university`
        WHERE universityName = '{university_name}' AND faculty = '{faculty}'
    """
    return query_bigquery(query)


@app.get("/languages/{university_name}/{faculty}/{department}")
def list_program_languages(university_name: str, faculty: str, department: str):
    """Returns a list of available languages for the selected department."""
    query = f"""
        SELECT DISTINCT language
        FROM `bitescout-445308.big_data.university`
        WHERE universityName = '{university_name}'
        AND faculty = '{faculty}'
        AND departmentName = '{department}'
    """
    return query_bigquery(query)


@app.get("/scholarships/{university_name}/{faculty}/{department}/{language}")
def list_scholarship_rates(university_name: str, faculty: str, department: str, language: str):
    """Returns available scholarship rates for the selected program."""
    query = f"""
        SELECT DISTINCT scholarshipRate
        FROM `bitescout-445308.big_data.university`
        WHERE universityName = '{university_name}'
        AND faculty = '{faculty}'
        AND departmentName = '{department}'
        AND language = '{language}'
    """
    return query_bigquery(query)


@app.post("/predict/")
def predict_program(user_input: UserInput):
    """Returns filtered university programs based on user selection."""
    query = f"""
        SELECT *
        FROM `bitescout-445308.big_data.university`
        WHERE universityName = '{user_input.university_name}'
        AND faculty = '{user_input.faculty}'
        AND departmentName = '{user_input.department}'
        AND scholarshipRate = {user_input.scholarship_rate}
        AND language = '{user_input.language}'
    """
    results = query_bigquery(query)

    
    if not results:
        raise HTTPException(status_code=404, detail="No matching department found.")

    return results
