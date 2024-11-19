from fastapi import FastAPI
from controllers import waste_item_controller
import pymongo
import os

app = FastAPI()

client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DATABASE_NAME")]

app.include_router(waste_item_controller.router, prefix="/waste-items", tags=["waste-items"])


