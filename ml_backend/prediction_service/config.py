from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BIGQUERY_DATASET: str = 'string_dataset'
    GOOGLE_APPLICATION_CREDENTIALS: str = 'bigquery_service_account.json'
    MODEL_PATH: str = 'xgb_model.pkl'
    # API Settings
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "University Ranking Prediction API"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()