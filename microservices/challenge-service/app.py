from fastapi import FastAPI
from controllers import challenge_controller
import pymongo
import os

app = FastAPI()

client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DATABASE_NAME")]

app.include_router(challenge_controller.router, prefix="/challenges", tags=["challenges"])
