import pandas as pd
from database import database_manager
from ml_model import model_manager
from models import UserInputModel, PredictionResponseModel
from fastapi import HTTPException
from loguru import logger

class PredictionService:
    """Service for handling university ranking predictions."""
    
    @staticmethod
    def predict_ranking(user_input: UserInputModel) -> PredictionResponseModel:
        """
        Predict university ranking based on input parameters.
        
        Args:
            user_input (UserInputModel): Input parameters for prediction
        
        Returns:
            PredictionResponseModel: Prediction results
        """
        try:
            # Find idOSYM using input parameters
            id_query = f"""
                SELECT idOSYM
                FROM `string_dataset.uni_list`
                WHERE academicYear = 2024
                AND universityName = '{user_input.university_name}'
                AND faculty = '{user_input.faculty}'
                AND departmentName = '{user_input.department}'
                AND scholarshipRate = {user_input.scholarship_rate}
                AND language = '{user_input.language}'
            """
            id_results = database_manager.execute_query(id_query)
            
            if not id_results:
                raise HTTPException(status_code=404, detail="No matching department found")
            
            id_OSYM = id_results[0]['idOSYM']
            
            # Retrieve scaled data for prediction
            data_query = f"""
                SELECT *
                FROM `string_dataset.uni_list_scaled`
                WHERE academicYear_flag = 2025
                AND idOSYM_flag = {id_OSYM}
            """
            data_results = database_manager.execute_query(data_query)
            
            if not data_results:
                raise HTTPException(status_code=404, detail="No prediction data available")
            print(data_results)
            # Prepare data for prediction
            result_df = pd.DataFrame(data_results)
            result_df = result_df.astype(float)
            result_df = result_df.drop(columns=["baseRanking", "academicYear_flag", "idOSYM_flag"])
            print(result_df.shape)
            # Predict ranking
            prediction = model_manager.predict(result_df)
            
            return PredictionResponseModel(
                prediction=float(prediction),
                metadata={
                    "university": user_input.university_name,
                    "department": user_input.department
                }
            )
        
        except Exception as e:
            logger.error(f"Prediction service error: {e}")
            raise