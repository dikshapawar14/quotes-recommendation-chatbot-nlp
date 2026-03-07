"""
Main Server File - FastAPI server setup
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routes - ab ye sahi se kaam karega
from app.backend.routes import router

# Create FastAPI app
app = FastAPI(
    title="Quote Recommendation Chatbot",
    description="Quote Recommendation Chatbot API using NLP",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": "Quote Recommendation Chatbot",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

if __name__ == "__main__":
    uvicorn.run(
        "app.backend.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )