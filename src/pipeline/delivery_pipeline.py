from src.ingestion.api_ingestion import run_ingestion
from src.bronze.bronze_loader import save_bronze
from src.transformation.transform import transform_data
from src.db.repository import load_data


def run_pipeline():
    data = run_ingestion()

    save_bronze(data)

    df = transform_data(data)
    load_data(df)

    print("Pipeline executada com sucesso!")
