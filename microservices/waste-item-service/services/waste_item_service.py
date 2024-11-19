from aiocache import Cache
from middleware.error_handler import handle_error, handle_invalid_id, handle_not_found
from bson import ObjectId
from bson.errors import InvalidId
import pymongo
import os

class WasteItemService:
    def __init__(self):
        try:
            client = pymongo.MongoClient(os.getenv("MONGO_URL"))
            self.db = client[os.getenv("DATABASE_NAME")]
            self.collection = self.db["waste_items"]
            self.cache = Cache.from_url("memory://")
        except Exception as e:
            handle_error("Database connection error", e)

    async def get_all_items(self):
        try:
            cached_items = await self.cache.get("all_items")
            if cached_items:
                return cached_items  
            items = list(self.collection.find())
            await self.cache.set("all_items", [{**item, "_id": str(item["_id"])} for item in items], ttl=60)
            return [{**item, "_id": str(item["_id"])} for item in items]
        except Exception as e:
            handle_error("Error fetching items", e)

    async def create_item(self, item):
        try:
            item_data = item.dict()
            result = self.collection.insert_one(item_data)
            item_data["_id"] = str(result.inserted_id)
            await self.cache.delete("all_items")
            return item_data
        except Exception as e:
            handle_error("Error creating item", e)

    async def get_item(self, item_id):
        try:
            item = self.collection.find_one({"_id": ObjectId(item_id)})
            if item:
                return {**item, "_id": str(item["_id"])}
            handle_not_found("Item not found")
        except InvalidId:
            handle_invalid_id("Invalid item ID format")
        except Exception as e:
            handle_error("Error fetching item", e)

    async def update_item(self, item_id, item):
        try:
            result = self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
            if result.modified_count == 1:
                await self.cache.delete("all_items")
                return {"message": "Item updated successfully"}
            handle_not_found("Item not found")
        except InvalidId:
            handle_invalid_id("Invalid item ID format")
        except Exception as e:
            handle_error("Error updating item", e)

    async def delete_item(self, item_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(item_id)})
            if result.deleted_count == 1:
                await self.cache.delete("all_items")
                return {"message": "Item deleted successfully"}
            handle_not_found("Item not found")
        except InvalidId:
            handle_invalid_id("Invalid item ID format")
        except Exception as e:
            handle_error("Error deleting item", e)
