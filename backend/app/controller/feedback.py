from fastapi import APIRouter
from datetime import datetime
from app.models.feedback import Feedback
from app.services.db import feedback_collection

router = APIRouter()

@router.post("/feedback")
def submit_feedback(feedback: Feedback):
    # Add timestamp
    feedback_dict = feedback.mode_dump()
    feedback_dict["created_at"] = datetime.now(datetime.timezone.utc)

    # Insert into MongoDB
    feedback_collection.insert_one(feedback_dict)
    return {"status": "success", "message": "Feedback saved"}
