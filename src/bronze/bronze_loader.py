import json
from datetime import datetime
from pathlib import Path


def save_bronze(data):
    date = datetime.now().strftime("%Y-%m-%d")

    folder = Path("data/bronze")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"users_{date}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path
