from airflow.decorators import dag, task
from datetime import datetime
import logging

from tasks.extract_hdb import extract_hdb_resale
from tasks.transform_hdb import transform_hdb
from tasks.load_hdb import load_hdb

# Default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2025, 1, 1),
}

# Define the DAG with TaskFlow API
@dag(
    dag_id='housing_sg__etl_pipeline__weekly',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False,
    tags=['housing', 'etl', 'singapore'],
    description='ETL pipeline for Singapore housing price data',
)
def housing_etl_pipeline():
    @task
    def extract_data():
        logging.info("Extracting data from HDB, URA, SingStat, and PropertyGuru APIs...")
        return {"hdb": "data", "ura": "data", "econ": "data", "pg": "data"}

    @task
    def transform_data(raw_data):
        logging.info("Cleaning, merging, and standardizing datasets...")
        # You can access raw_data["hdb"], etc.
        return {"transformed_data": "result"}

    @task
    def load_data(data):
        logging.info("Saving transformed data to storage/database...")
        # Save logic here
        logging.info(f"Data loaded: {data}")

    hdb_path = extract_hdb_resale()
    transformed_hdb_path = transform_hdb(hdb_path)
    load_hdb(transformed_hdb_path)

    # Task chaining
    extracted = extract_data()
    transformed = transform_data(extracted)
    load_data(transformed)

# Assign to a DAG object so Airflow can detect it
housing_etl_pipeline = housing_etl_pipeline()
