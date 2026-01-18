from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.models.feedback import Feedback
from app.services.db import feedback_collection, get_database
from app.services.feedback_processor import analyze_and_fix_feedback

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

        # Process feedback with AI
        ai_result = analyze_and_fix_feedback(feedback)

        return {
            "status": "success",
            "message": "Feedback saved and processed",
            "id": str(result.inserted_id),
            "ai_result": ai_result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save feedback: {str(e)}"
        )

