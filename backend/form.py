from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Atlas
MONGO_URI = "mongodb+srv://zhtmichelle_db_user:tPwROf6KxSIKURYU@nwhacks26.exsxsye.mongodb.net/?appName=nwhacks26"
client = MongoClient(MONGO_URI)
db = client.feedbackDB
feedback_collection = db.feedbacks  # Collection to store feedback

# Feedback schema
class Feedback(BaseModel):
    name: str
    email: str
    message: str

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    # Add timestamp
    feedback_dict = feedback.mode_dump()
    feedback_dict["created_at"] = datetime.now(datetime.timezone.utc)

    # Insert into MongoDB
    feedback_collection.insert_one(feedback_dict)
    return {"status": "success", "message": "Feedback saved"}
