import os
from dotenv import load_dotenv
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

load_dotenv()  # Load variables from .env

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
feedback_collection = db.feedbacks


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
