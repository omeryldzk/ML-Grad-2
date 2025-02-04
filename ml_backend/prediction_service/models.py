from pydantic import BaseModel, Field, validator
from typing import Optional

class UserInputModel(BaseModel):
    """Input model for university ranking prediction"""
    university_name: str = Field(..., min_length=2, max_length=100)
    faculty: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)
    language: str = Field(..., min_length=2, max_length=50)
    scholarship_rate: float = Field(...,  ge=0,le=100,description="Scholarship rate percentage (0-100)")
    @validator('university_name', 'faculty', 'department', 'language')
    def strip_and_validate(cls, v):
        """Strip whitespace and validate non-empty strings"""
        v = v.strip()
        if not v:
            raise ValueError('Field cannot be empty')
        return v

class PredictionResponseModel(BaseModel):
    """Response model for prediction results"""
    prediction: float
    confidence: Optional[float] = None
    metadata: Optional[dict] = None