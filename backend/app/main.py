from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seeder import seed_database
from app.routers import requests, resources, volunteers, hospital, websocket

# Lifespan context for startup seeding and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed initial data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Emergency Resource Coordination Platform with Real-Time Dispatch and Map Radar",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(requests.router)
app.include_router(resources.router)
app.include_router(volunteers.router)
app.include_router(hospital.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {
        "platform": "LifeLink",
        "tagline": "Coordinating the entire emergency response quickly",
        "status": "online",
        "docs": "/docs",
        "city": "Bhubaneswar"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "LifeLink Backend API"}
