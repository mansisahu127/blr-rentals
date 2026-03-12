from app.db.database import get_connection
from app.services.embeddings import get_query_embedding

def search_listings(
    query: str,
    limit: int = 6,
    max_rent: int = None,
    bhk: str = None,
    location: str = None,
    brokerage: bool = None,
    amenities: list[str] = None
) -> list[dict]:
    """Semantic search with optional hard filters."""

    query_embedding = get_query_embedding(query)

    filters = []
    params = [query_embedding, query_embedding]

    if max_rent:
        filters.append("rent <= %s")
        params.append(max_rent)
    if bhk:
        filters.append("bhk ILIKE %s")
        params.append(bhk)
    if location:
        filters.append("location ILIKE %s")
        params.append(f"%{location}%")
    if brokerage is not None:
        filters.append("brokerage = %s")
        params.append(brokerage)
    if amenities:
        filters.append("amenities && %s")
        params.append(amenities)

    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    params.append(limit)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT
            id, source, location, rent, bhk,
            amenities, contact, posted_at, brokerage,
            1 - (embedding <=> %s::vector) AS similarity
        FROM listings
        {where}
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, params)

    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results