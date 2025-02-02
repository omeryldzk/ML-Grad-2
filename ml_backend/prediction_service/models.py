from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define request structure (User input model)
class UserInput(BaseModel):
    university_name: str
    faculty: str
    department: str
    scholarship_rate: float
    language: str
