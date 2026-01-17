from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client[os.getenv('MONGO_DB')]
feedback_collection = db.feedbacks
