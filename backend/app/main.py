from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.migrations import run_migrations
from app.api.v1.routers import chat, listings, ingest
# Import the scheduler from your ingest router
from app.api.v1.routers.ingest import start_scheduler

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    # Keep your refined origins here for security!
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # 1. Run DB migrations
    run_migrations()
    
    # 2. Start the background scrapers
    try:
        # start_scheduler()
        print("Background Scheduler initialized")
    except Exception as e:
        print(f"Failed to start scheduler: {e}")
        
    print(f"🚀 {settings.app_name} is running")

app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["Chat"]
)
app.include_router(
    listings.router,
    prefix="/api/v1",
    tags=["Listings"]
)
app.include_router(
    ingest.router,
    prefix="/api/v1",
    tags=["Ingestion"]
)

@app.get("/")
async def root():
    return {"status": "ok", "message": f"🏠 {settings.app_name}"}

@app.get("/health")
async def health():
    return {"status": "healthy"}