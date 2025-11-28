"""
BeatCanvas FastAPI Application
Main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router


# Create FastAPI application
app = FastAPI(
    title="BeatCanvas API",
    description="AI-powered music generation API using OpenAI and Python audio processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Next.js default port
        "http://127.0.0.1:3000",      # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
    expose_headers=["X-Tempo", "X-Bars", "X-Key", "X-Scale"]  # Custom metadata headers
)

# Include API routes
app.include_router(router, prefix="/api", tags=["music"])


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to BeatCanvas API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


# For local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
