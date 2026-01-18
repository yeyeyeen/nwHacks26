from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConfigurationError, ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI')
MONGO_DB = os.getenv('MONGO_DB', 'feedbackDB')  # Default database name

# Validate MongoDB URI is set
if not MONGODB_URI:
    logger.error("✗ MONGODB_URI environment variable is not set!")
    logger.warning("⚠ Please add MONGODB_URI to your .env file")

# Initialize client with lazy connection
client = None
db = None
feedback_collection = None

def get_database():
    """Get database instance with lazy initialization and error handling"""
    global client, db, feedback_collection

    if client is None:
        if not MONGODB_URI:
            logger.error("✗ Cannot connect to MongoDB: MONGODB_URI not configured")
            return None

        try:
            logger.info("Attempting to connect to MongoDB...")
            # Mask sensitive parts of URI for logging
            masked_uri = MONGODB_URI.split('@')[0].split('://')[0] + "://****@" + MONGODB_URI.split('@')[1] if '@' in MONGODB_URI else "****"
            logger.debug(f"MongoDB URI: {masked_uri}")

            # serverSelectionTimeoutMS prevents hanging on connection issues
            client = MongoClient(
                MONGODB_URI,
                server_api=ServerApi('1'),
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
        except OperationFailure as e:
            # Authentication errors
            if "authentication failed" in str(e).lower() or e.code == 8000:
                logger.error(f"✗ MongoDB authentication failed!")
                logger.error("✗ The username or password in your MONGODB_URI is incorrect")
                logger.warning("⚠ To fix this:")
                logger.warning("  1. Go to MongoDB Atlas → Database Access")
                logger.warning("  2. Verify your database user exists")
                logger.warning("  3. Reset the password if needed")
                logger.warning("  4. Update MONGODB_URI in your .env file")
                logger.warning("  5. Make sure to URL-encode special characters in the password")
            else:
                logger.error(f"✗ MongoDB operation failed: {e}")
            logger.warning("⚠ Application will start but database operations will fail")
            return None
        except (ConfigurationError, ConnectionFailure) as e:
            logger.error(f"✗ MongoDB connection failed: {e}")
            logger.warning("⚠ Application will start but database operations will fail")
            logger.warning("⚠ Please check your .env file and ensure MONGODB_URI is correct")
            # Return None to allow app to start without DB
            return None
        except Exception as e:
            logger.error(f"✗ Unexpected error connecting to MongoDB: {e}")
            logger.warning("⚠ Check your MongoDB configuration")
            return None

    return db

# Try to connect on import, but don't fail if it doesn't work
get_database()

