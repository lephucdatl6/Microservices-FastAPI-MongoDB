from fastapi import FastAPI
from controllers import waste_category_controller
import pymongo
import os

app = FastAPI()

client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DATABASE_NAME")]

app.include_router(waste_category_controller.router, prefix="/waste-categories", tags=["waste-categories"])
