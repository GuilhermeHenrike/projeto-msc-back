import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg.connect(
        os.getenv("DATABASE_URL"),
        row_factory=dict_row
    )