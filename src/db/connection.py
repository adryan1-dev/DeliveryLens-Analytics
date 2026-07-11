import psycopg2
import src.config.settings as cs

def get_connection():
    return psycopg2.connect(
        dbname=cs.DB_NAME,
        user=cs.DB_USER,
        password=cs.DB_PASSWORD,
        host=cs.DB_HOST,
        port=cs.DB_PORT
    )