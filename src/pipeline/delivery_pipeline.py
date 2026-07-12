from src.ingestion.api_ingestion import run_ingestion
from src.bronze.bronze_loader import save_bronze
from src.silver.silver_transformer import transform_to_silver, load_valid_silver_records
from src.transformation.transform import transform_data
from src.db.repository import load_data


def run_pipeline():
    data = run_ingestion()

    save_bronze(data)
    silver_file_path = transform_to_silver()

    valid_records = load_valid_silver_records(silver_file_path)
    df = transform_data(valid_records)
    load_data(df)

    print("Pipeline executada com sucesso!")