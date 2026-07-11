import pandas as pd
from src.db.connection import get_connection


def load_data(df):
    connection = get_connection()

    cursor = connection.cursor()
    
    cursor.execute(
        "TRUNCATE TABLE deliveries_test"
    )

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO deliveries_test
            (id, name, username, email)
            VALUES (%s, %s, %s, %s)
            """,
            (
                row["id"],
                row["name"],
                row["username"],
                row["email"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()