from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ConnectionFailure
import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

# MongoDB configuration
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER')
MONGO_DB = os.getenv('MONGO_DB')

# Build MongoDB URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"

# Initialize client with lazy connection (connect=False prevents immediate connection attempt)
client = None
db = None
feedback_collection = None

def get_database():
    """Get database instance with lazy initialization and error handling"""
    global client, db, feedback_collection

    if client is None:
        try:
            logger.info("Attempting to connect to MongoDB...")
            logger.debug(f"MongoDB URI: mongodb+srv://{MONGO_USER}:****@{MONGO_CLUSTER}/{MONGO_DB}")

            # serverSelectionTimeoutMS prevents hanging on connection issues
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            # Test the connection
            client.admin.command('ping')
            db = client[MONGO_DB]
            feedback_collection = db.feedbacks

            logger.info("✓ MongoDB connected successfully")
            logger.info(f"✓ Using database: {MONGO_DB}")
            logger.info(f"✓ Using collection: feedbacks")
        except (ConfigurationError, ConnectionFailure) as e:
            logger.error(f"✗ MongoDB connection failed: {e}")
            logger.error(f"✗ MONGO_CLUSTER: {MONGO_CLUSTER}")
            logger.warning("⚠ Application will start but database operations will fail")
            logger.warning("⚠ Please check your .env file and ensure MONGO_CLUSTER is correct")
            # Return None to allow app to start without DB
            return None
        except Exception as e:
            logger.error(f"✗ Unexpected error connecting to MongoDB: {e}")
            return None

    return db

# Try to connect on import, but don't fail if it doesn't work
get_database()
