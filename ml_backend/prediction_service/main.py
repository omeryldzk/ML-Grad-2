from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from models import UserInputModel, PredictionResponseModel
from prediction_service import PredictionService
from database import database_manager

# Configure logging
logger.add("app.log", rotation="10 MB")

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/predict", response_model=PredictionResponseModel)
def predict_ranking(user_input: UserInputModel):
    """University ranking prediction endpoint."""
    return PredictionService.predict_ranking(user_input)

@app.get("/universities")
def list_universities():
    """Retrieve list of available universities."""
    return database_manager.get_universities()

@app.get("/faculties/{university_name}")
def list_faculties(university_name: str):
    """Retrieve list of faculties for a specific university."""
    return database_manager.get_faculties(university_name)

@app.get("/departments/{university_name}/{faculty}")
def list_departments(university_name: str, faculty: str):
    """Retrieve list of departments for a specific faculty and university."""
    return database_manager.get_departments(university_name, faculty)

@app.get("/languages/{university_name}/{faculty}/{department}")
def list_languages(university_name: str, faculty: str, department: str):
    """Retrieve list of languages for a specific department."""
    return database_manager.get_languages(university_name, faculty, department)

@app.get("/scholarships/{university_name}/{faculty}/{department}/{language}")
def list_scholarships(university_name: str, faculty: str, department: str, language: str):
    """Retrieve list of scholarship rates for a specific program."""
    return database_manager.get_scholarships(university_name, faculty, department, language)
