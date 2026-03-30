from fastapi import APIRouter, BackgroundTasks, Depends
from app.schemas.listing import IngestRequest
from app.services.ingestion import ingest_listing
from app.scraper.nobroker import scrape_nobroker
from app.db.database import get_connection

router = APIRouter()

# ... your other imports ...
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scraper.nobroker import scrape_nobroker

router = APIRouter()
scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            scrape_nobroker,
            trigger="interval",
            hours=24,
            id="nobroker_scraper",
            replace_existing=True
        )
        # Add other scrapers here if needed
        scheduler.start()
        print("✅ Scheduler started — all scrapers active")

@router.post("/ingest")
async def ingest(payload: IngestRequest):
    source_id = payload.source_id or payload.raw_text[:60]
    # Assuming ingest_listing is a sync function, if async, use 'await'
    success = ingest_listing(payload.raw_text, payload.source, source_id)
    return {"success": success, "source_id": source_id}

@router.post("/ingest/nobroker")
async def ingest_nobroker(background_tasks: BackgroundTasks):
    # Using background_tasks to run the async scraper
    background_tasks.add_task(scrape_nobroker)
    return {"status": "started", "source": "nobroker"}

@router.post("/ingest/all")
async def ingest_all(background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_nobroker)
    return {
        "status": "started", 
        "sources": ["nobroker"]
    }

@router.get("/ingest/status")
async def ingest_status():
    conn = get_connection()
    cur = conn.cursor()
    # Using fetchall() and converting to list of dicts for JSON safety
    cur.execute("""
        SELECT source, COUNT(*) as count, MAX(created_at) as last_ingested
        FROM listings 
        GROUP BY source
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"source": r[0], "count": r[1], "last_ingested": str(r[2])} for r in rows]