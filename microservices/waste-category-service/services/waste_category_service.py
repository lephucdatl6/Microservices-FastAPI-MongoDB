from aiocache import Cache
from middleware.error_handler import handle_error, handle_invalid_id, handle_not_found
from bson import ObjectId
from bson.errors import InvalidId
import pymongo
import os

class WasteCategoryService:
    def __init__(self):
        try:
            client = pymongo.MongoClient(os.getenv("MONGO_URL"))
            self.db = client[os.getenv("DATABASE_NAME")]
            self.collection = self.db["waste_categories"]
            self.cache = Cache.from_url("memory://")
        except Exception as e:
            handle_error("Database connection error", e)

    async def get_all_categories(self):
        try:
            cached_categories = await self.cache.get("all_categories")
            if cached_categories:
                return cached_categories
            categories = list(self.collection.find())
            await self.cache.set("all_categories", [{**category, "_id": str(category["_id"])} for category in categories], ttl=60)
            return [{**category, "_id": str(category["_id"])} for category in categories]
        except Exception as e:
            handle_error("Error fetching categories", e)

    async def create_category(self, category):
        try:
            category_data = category.dict()
            result = self.collection.insert_one(category_data)
            category_data["_id"] = str(result.inserted_id)
            await self.cache.delete("all_categories")
            return category_data
        except Exception as e:
            handle_error("Error creating category", e)

    async def get_category(self, category_id):
        try:
            category = self.collection.find_one({"_id": ObjectId(category_id)})
            if category:
                return {**category, "id": str(category["_id"])}
            handle_not_found("Category not found")
        except InvalidId:
            handle_invalid_id("Invalid category ID format")
        except Exception as e:
            handle_error("Error fetching category", e)

    async def update_category(self, category_id, category):
        try:
            result = self.collection.update_one({"_id": ObjectId(category_id)}, {"$set": category.dict()})
            if result.modified_count == 1:
                await self.cache.delete("all_categories")
                return {"message": "Category updated successfully"}
            handle_not_found("Category not found")
        except InvalidId:
            handle_invalid_id("Invalid category ID format")
        except Exception as e:
            handle_error("Error updating category", e)

    async def delete_category(self, category_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(category_id)})
            if result.deleted_count == 1:
                await self.cache.delete("all_categories")
                return {"message": "Category deleted successfully"}
            handle_not_found("Category not found")
        except InvalidId:
            handle_invalid_id("Invalid category ID format")
        except Exception as e:
            handle_error("Error deleting category", e)
