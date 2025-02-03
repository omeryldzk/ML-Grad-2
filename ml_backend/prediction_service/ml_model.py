import joblib
import pandas as pd
import numpy as np
from loguru import logger
from config import settings

class ModelManager:
    """Manages machine learning model loading and prediction."""
    
    def __init__(self):
        """Load pre-trained model."""
        try:
            # Load the saved dictionary
            model_data = joblib.load(settings.MODEL_PATH)

            # Ensure it's a dictionary and extract the model
            if not isinstance(model_data, dict) or 'model' not in model_data:
                raise ValueError("Invalid model file format. Expected a dictionary with a 'model' key.")

            self.model = model_data['model']

            # Check if it's a valid model
            if not hasattr(self.model, 'predict'):
                raise AttributeError("Loaded object is not a valid predictive model")

        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise

    def predict(self, input_data):
        """Generate prediction from input data."""
        try:
            if not isinstance(input_data, pd.DataFrame):
                raise TypeError("Input must be a pandas DataFrame")
            
            prediction = self.model.predict(input_data)
            return prediction[0] if len(prediction) > 0 else None

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            logger.error(f"Input data shape: {input_data.shape}")
            logger.error(f"Input data columns: {input_data.columns}")
            raise

# Model manager instance
model_manager = ModelManager()
