from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from src.pipeline.delivery_pipeline import run_pipeline


def execute_pipeline():
    run_pipeline()


with DAG(
    dag_id="deliverylens_pipeline",
    start_date=datetime(2026, 7, 9),
    schedule="@daily",
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id="run_deliverylens_pipeline",
        python_callable=execute_pipeline
    )