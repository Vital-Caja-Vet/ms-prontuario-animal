import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def create_database_if_not_exists():
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/ms_prontuario_animal')
    db_name = db_url.rsplit('/', 1)[-1]  # "ms_prontuario_animal"

    # Conecta no postgres padrão
    conn = psycopg2.connect("dbname=postgres user=postgres password=root host=localhost port=5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f'CREATE DATABASE {db_name};')
        print(f"Banco {db_name} criado automaticamente!")

    cur.close()
    conn.close()
