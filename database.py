# database.py
import os
from psycopg2 import pool
from dotenv import load_dotenv

# Carga las variables desde .env (si existe)
load_dotenv()

# Configuración de conexión — usa valores por defecto si no hay .env
DB_NAME = os.getenv("DB_NAME", "petmarket")
DB_USER = os.getenv("DB_USER", "postgres")  # ← tu usuario real
DB_PASS = os.getenv("DB_PASS", "postgres")  # ← reemplaza con tu contraseña de pgAdmin
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

_db_pool = None

def init_db_pool(minconn=1, maxconn=5):
    """Inicializa un pool de conexiones a la base de datos."""
    global _db_pool
    if _db_pool is None:
        _db_pool = pool.SimpleConnectionPool(
            minconn, maxconn,
            dbname=DB_NAME, user=DB_USER, password=DB_PASS,
            host=DB_HOST, port=DB_PORT
        )
    return _db_pool

def get_conn():
    """Obtiene una conexión del pool."""
    global _db_pool
    if _db_pool is None:
        init_db_pool()
    return _db_pool.getconn()

def put_conn(conn):
    """Devuelve una conexión al pool."""
    global _db_pool
    if _db_pool:
        _db_pool.putconn(conn)
