from db.connection import get_connection


def run_ingestion():
    conn = get_connection()

    print("Conexão realizada com sucesso!")

    conn.close()