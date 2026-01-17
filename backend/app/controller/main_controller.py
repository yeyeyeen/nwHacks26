from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app import app

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Simple FastAPI REST Controller"}

