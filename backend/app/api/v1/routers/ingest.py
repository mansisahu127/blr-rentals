from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def ingest_data():
    return {"message": "Ingest route working"}