import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from app.core.config import settings

def get_connection():
    conn = psycopg2.connect(
        settings.database_url,
        cursor_factory=RealDictCursor
    )
    register_vector(conn)
    return conn
