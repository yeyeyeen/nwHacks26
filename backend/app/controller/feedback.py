from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.models.feedback import Feedback
from app.services.db import feedback_collection, get_database

router = APIRouter()

@router.post("/feedback")
def submit_feedback(feedback: Feedback):
    # Ensure database is connected
    if feedback_collection is None:
        # Try to reconnect
        get_database()
        if feedback_collection is None:
            raise HTTPException(
                status_code=503,
                detail="Database connection unavailable. Please check your MongoDB configuration."
            )

    try:
        # Add timestamp
        feedback_dict = feedback.model_dump()
        feedback_dict["created_at"] = datetime.now(timezone.utc)

        # Insert into MongoDB
        result = feedback_collection.insert_one(feedback_dict)
        return {
            "status": "success",
            "message": "Feedback saved",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save feedback: {str(e)}"
        )

