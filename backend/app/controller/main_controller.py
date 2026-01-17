from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    """Root endpoint"""
    return {"message": "Simple FastAPI REST Controller"}

