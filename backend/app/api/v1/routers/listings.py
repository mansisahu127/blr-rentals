from fastapi import APIRouter, Query
from typing import Optional, List
from app.db.database import get_connection

router = APIRouter()

# Entry point for retrieving rental listings with optional filters
@router.get("/listings")
async def get_listings(
    location: Optional[str] = Query(None),
    max_rent: Optional[int] = Query(None),
    bhk: Optional[str] = Query(None),
    brokerage: Optional[bool] = Query(None),
    amenities: Optional[List[str]] = Query(None), 
    limit: int = Query(20, le=100)
):
    conn = get_connection()
    cur = conn.cursor()

    filters, params = [], []

    # Apply filters based on query parameters
    if location:
        filters.append("location ILIKE %s")
        params.append(f"%{location}%")
    if max_rent:
        filters.append("rent <= %s")
        params.append(max_rent)
    if bhk:
        filters.append("bhk ILIKE %s")
        params.append(bhk)
    if brokerage is not None:
        filters.append("brokerage = %s")
        params.append(brokerage)
    if amenities:
        filters.append("amenities && %s")
        params.append(amenities)

    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    params.append(limit)

    cur.execute(f"""
        SELECT id, source, location, rent, bhk, brokerage, amenities, contact, posted_at
        FROM listings {where}
        ORDER BY posted_at DESC LIMIT %s
    """, params)

    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()

    for r in results:
        if r.get("posted_at"):
            r["posted_at"] = str(r["posted_at"])

    return results

# Entry point for retrieving stats about the listings database
@router.get("/listings/stats")
async def get_stats():
    conn = get_connection()
    cur = conn.cursor()

    # Aggregate stats about listings
    cur.execute("""
        SELECT
            COUNT(*) as total,
            COUNT(DISTINCT source) as sources,
            ROUND(AVG(rent)) as avg_rent,
            MAX(posted_at) as last_updated
        FROM listings
    """)
    stats = dict(cur.fetchone())
    cur.close()
    conn.close()

    if stats.get("last_updated"):
        stats["last_updated"] = str(stats["last_updated"])
    return stats
