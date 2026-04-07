from app.db.database import get_connection

def run_migrations():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source      TEXT NOT NULL,
            raw_text    TEXT NOT NULL,
            location    TEXT,
            rent        INTEGER,
            bhk         TEXT,
            brokerage   BOOLEAN,
            amenities   TEXT[],
            contact     TEXT,
            posted_at   TIMESTAMP DEFAULT NOW(),
            source_id   TEXT UNIQUE,
            embedding   vector(384)
        );
    """)

    # Rebuild index — drop the old one (lists=100 is too high for small datasets)
    cur.execute("DROP INDEX IF EXISTS listings_embedding_idx;")
    cur.execute("""
        CREATE INDEX listings_embedding_idx
        ON listings USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 10);
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Migrations complete")
    