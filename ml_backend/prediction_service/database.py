from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client.from_service_account_json("service-account.json")

DATASET_ID = "university_data"
TABLE_ID = "departments"

def query_bigquery(query: str):
    """Executes a query and returns the result as a list of dictionaries."""
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]

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
