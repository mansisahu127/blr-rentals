from fastapi import APIRouter, BackgroundTasks
from app.schemas.listing import IngestRequest
from app.services.ingestion import ingest_listing

router = APIRouter()

# Entry point for ingesting new rental listings into the system.
@router.post("/ingest")
async def ingest(payload : IngestRequest) :
    # Idempotency logic: Use provided source_id or fallback to a snippet of the raw text.
    source_id = payload.source_id or payload.raw_text[:60] 

    # Pass data to the service layer which handles LLM parsing, embedding, and DB insertion.
    success = ingest_listing(payload.raw_text, payload.source, source_id)

    return {"success": success, "source_id": source_id}
