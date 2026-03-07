"""
API Routes
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "routes", "message": "API working!"}

@router.get("/test")
async def test():
    return {"message": "Routes working properly!"}

@router.get("/info")
async def info():
    return {
        "name": "Quote API",
        "version": "1.0",
        "endpoints": ["/health", "/test", "/info"]
    }