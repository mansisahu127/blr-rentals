import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from app.core.config import settings

def get_connection():
    try:
        # For Supabase/Cloud, sslmode='require' is mandatory
        conn = psycopg2.connect(
            settings.database_url,
            cursor_factory=RealDictCursor,
            sslmode='require' 
        )
        
        register_vector(conn)
        return conn
    except Exception as e:
        print(f"Connection to Supabase failed: {e}")
        raise