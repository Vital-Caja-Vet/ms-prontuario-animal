import os
from urllib.parse import urlparse

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


def _parse_database_url(db_url: str):
    parsed = urlparse(db_url)
    return {
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "dbname": (parsed.path or "/").lstrip("/") or None,
    }


def create_database_if_not_exists():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL não configurada no ambiente")

    info = _parse_database_url(db_url)
    db_name = info["dbname"]

    # Permite sobrescrever via variáveis dedicadas, mas por padrão usa os dados do DATABASE_URL
    admin_db = os.getenv("POSTGRES_ADMIN_DB", "postgres")
    admin_host = os.getenv("POSTGRES_HOST", info["host"])
    admin_port = int(os.getenv("POSTGRES_PORT", info["port"]))
    admin_user = os.getenv("POSTGRES_USER", info["user"])
    admin_password = os.getenv("POSTGRES_PASSWORD", info["password"])

    conn = psycopg2.connect(
        dbname=admin_db,
        user=admin_user,
        password=admin_password,
        host=admin_host,
        port=admin_port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Banco {db_name} criado automaticamente!")

    cur.close()
    conn.close()

