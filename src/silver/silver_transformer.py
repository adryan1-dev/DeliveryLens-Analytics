import json
from datetime import datetime
from pathlib import Path


def _find_latest_bronze_file():
    bronze_folder = Path("data/bronze")
    files = sorted(bronze_folder.glob("users_*.json"))

    if not files:
        raise FileNotFoundError("Nenhum arquivo encontrado em data/bronze")

    return files[-1]


def _validate_record(record):
    errors = []

    if not record.get("id"):
        errors.append("id ausente")

    if not record.get("name"):
        errors.append("name ausente ou vazio")

    email = record.get("email", "")
    if not email or "@" not in email:
        errors.append("email ausente ou invalido")

    return errors


def transform_to_silver():
    bronze_file = _find_latest_bronze_file()

    with open(bronze_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    silver_data = []

    for record in raw_data:
        errors = _validate_record(record)

        record["is_valid"] = len(errors) == 0
        record["validation_errors"] = errors

        silver_data.append(record)

    date = datetime.now().strftime("%Y-%m-%d")
    folder = Path("data/silver")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"users_{date}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(silver_data, file, indent=4)

    valid_count = sum(1 for r in silver_data if r["is_valid"])
    invalid_count = len(silver_data) - valid_count

    print(f"Silver Layer: {valid_count} registros validos, {invalid_count} invalidos")

    return file_path


def load_valid_silver_records(silver_file_path):
    with open(silver_file_path, "r", encoding="utf-8") as file:
        silver_data = json.load(file)

    valid_records = []
    for record in silver_data:
        if record["is_valid"]:
            record = record.copy()
            record.pop("is_valid")
            record.pop("validation_errors")
            valid_records.append(record)

    return valid_records
