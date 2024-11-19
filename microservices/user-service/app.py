from fastapi import FastAPI, HTTPException
from controllers.user_controllers import router as user_router
import logging
import pymongo
import os

os.environ["JWT_SECRET"] = "your_jwt_secret"

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    logger.info("Connected to MongoDB successfully.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise HTTPException(status_code=500, detail="Database connection error")

app.include_router(user_router, prefix="/users", tags=["users"])
