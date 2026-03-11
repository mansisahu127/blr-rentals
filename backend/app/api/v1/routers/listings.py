from fastapi import APIRouter

# This is the exact line the error is looking for
router = APIRouter()

@router.get("/")
async def get_all_listings():
    return {"message": "Listings route working"}