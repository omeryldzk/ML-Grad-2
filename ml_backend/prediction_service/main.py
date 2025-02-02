from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from bigquery import query_bigquery

app = FastAPI()




