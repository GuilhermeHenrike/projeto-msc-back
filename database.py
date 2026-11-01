import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def conectar():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não configurada!")

    return psycopg.connect(
        database_url,
        row_factory=dict_row,
        connect_timeout=10
    )