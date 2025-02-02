from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from bigquery import query_bigquery

app = FastAPI()

# Define request structure
class UserSelection(BaseModel):
    university_name: str
    faculty: str
    department: str
    scholarship_rate: float
    language: str


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
def predict_program(user_input: UserSelection):
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
