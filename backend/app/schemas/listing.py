from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ListingResponse(BaseModel):
    id: str
    source: str
    location: Optional[str]
    rent: Optional[int]
    brokerage: Optional[bool]
    bhk: Optional[str]
    amenities: Optional[List[str]]
    contact: Optional[str]
    posted_at: Optional[datetime]
    similarity: Optional[float] = None

class IngestRequest(BaseModel):
    raw_text: str
    source: str = "manual"
    source_id: Optional[str] = None