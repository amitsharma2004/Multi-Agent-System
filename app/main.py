from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from app.database import connect_to_mongo, close_mongo_connection
from app.controllers import auth_router, user_router, lead_router
from app.services.search import search_web, scrape_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Agentic Sales Outreach System",
    description="Autonomous B2B sales assistant with lead generation and personalized email drafting",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(lead_router)


# Pydantic models for search/scrape
class SearchQuery(BaseModel):
    query: str
    max_results: int = 5


class ScrapeRequest(BaseModel):
    url: str


@app.get("/")
def read_root():
    return {
        "message": "Agentic Sales Outreach System API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/search")
def search(request: SearchQuery):
    """Search the web using Tavily"""
    try:
        results = search_web(request.query, request.max_results)
        return results
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/scrape")
def scrape(request: ScrapeRequest):
    """Scrape a URL using Firecrawl"""
    try:
        result = scrape_url(request.url)
        return result
    except Exception as e:
        return {"error": str(e)}
