from google.cloud import bigquery
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations for university ranking prediction."""
    
    def __init__(self, service_account_path: str):
        """
        Initialize BigQuery client.
        
        Args:
            service_account_path (str): Path to service account JSON
        """
        try:
            self.client = bigquery.Client.from_service_account_json(service_account_path)
            self.dataset_id = "string_dataset"
        except Exception as e:
            logger.error(f"BigQuery initialization error: {e}")
            raise

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute BigQuery query and return results.
        
        Args:
            query (str): SQL query to execute
        
        Returns:
            List of dictionaries with query results
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def get_universities(self) -> List[str]:
        """
        Retrieve list of available universities.
        
        Returns:
            List of university names
        """
        query = f"SELECT DISTINCT universityName FROM `{self.dataset_id}.uni_list`"
        return [row['universityName'] for row in self.execute_query(query)]

    def get_faculties(self, university_name: str) -> List[str]:
        """
        Retrieve faculties for a specific university.
        
        Args:
            university_name (str): Name of the university
        
        Returns:
            List of faculty names
        """
        query = f"""
            SELECT DISTINCT faculty
            FROM `{self.dataset_id}.uni_list`
            WHERE universityName = '{university_name}'
        """
        return [row['faculty'] for row in self.execute_query(query)]

    def get_departments(self, university_name: str, faculty: str) -> List[str]:
        """
        Retrieve departments for a specific university and faculty.
        
        Args:
            university_name (str): Name of the university
            faculty (str): Name of the faculty
        
        Returns:
            List of department names
        """
        query = f"""
            SELECT DISTINCT departmentName
            FROM `{self.dataset_id}.uni_list`
            WHERE universityName = '{university_name}'
            AND faculty = '{faculty}'
        """
        return [row['departmentName'] for row in self.execute_query(query)]

    def get_languages(self, university_name: str, faculty: str, department: str) -> List[str]:
        """
        Retrieve available languages for a specific university, faculty, and department.
        
        Args:
            university_name (str): Name of the university
            faculty (str): Name of the faculty
            department (str): Name of the department
        
        Returns:
            List of language names
        """
        query = f"""
            SELECT DISTINCT language
            FROM `{self.dataset_id}.uni_list`
            WHERE universityName = '{university_name}'
            AND faculty = '{faculty}'
            AND departmentName = '{department}'
        """
        return [row['language'] for row in self.execute_query(query)]

    def get_scholarship_rates(
        self, 
        university_name: str, 
        faculty: str, 
        department: str, 
        language: str
    ) -> List[float]:
        """
        Retrieve available scholarship rates for a specific program.
        
        Args:
            university_name (str): Name of the university
            faculty (str): Name of the faculty
            department (str): Name of the department
            language (str): Program language
        
        Returns:
            List of scholarship rates
        """
        query = f"""
            SELECT DISTINCT scholarshipRate
            FROM `{self.dataset_id}.uni_list`
            WHERE universityName = '{university_name}'
            AND faculty = '{faculty}'
            AND departmentName = '{department}'
            AND language = '{language}'
        """
        return [row['scholarshipRate'] for row in self.execute_query(query)]

# Global database manager instance
database_manager = DatabaseManager("bigquery_service_account.json")