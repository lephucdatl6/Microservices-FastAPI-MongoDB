from aiocache import Cache
from middleware.error_handler import handle_error, handle_invalid_id, handle_not_found
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
import jwt
import datetime
import pymongo
import os

class UserService:
    def __init__(self):
        try:
            client = pymongo.MongoClient(os.getenv("MONGO_URL"))
            self.db = client[os.getenv("DATABASE_NAME")]
            self.collection = self.db["users"]
            self.cache = Cache.from_url("memory://")
        except Exception as e:
            handle_error("Database connection error", e)

    async def get_all_users(self):
        try:
            cached_users = await self.cache.get("all_users")
            if cached_users:
                return cached_users 
            users = list(self.collection.find())
            await self.cache.set("all_users", [{**user, "_id": str(user["_id"])} for user in users], ttl=60)
            return [{**user, "_id": str(user["_id"])} for user in users]
        except Exception as e:
            handle_error("Error fetching users", e)

    async def create_user(self, user):
        try:
            user_data = user.dict()
            result = self.collection.insert_one(user_data)
            user_data["_id"] = str(result.inserted_id)
            user_data = {"_id": user_data["_id"], **user_data}
            await self.cache.delete("all_users")
            return user_data
        except Exception as e:
            handle_error("Error creating user", e)

    async def get_user(self, user_id):
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return {**user, "_id": str(user["_id"])}
            handle_not_found("User not found")
        except InvalidId:
            handle_invalid_id("Invalid user ID format")
        except Exception as e:
            handle_error("Error fetching user", e)

    async def update_user(self, user_id, user):
        try:
            result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
            if result.modified_count == 1:
                await self.cache.delete("all_users")
                return {"message": "User updated successfully"}
            handle_not_found("User not found")
        except InvalidId:
            handle_invalid_id("Invalid user ID format")
        except Exception as e:
            handle_error("Error updating user", e)

    async def delete_user(self, user_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 1:
                await self.cache.delete("all_users")
                return {"message": "User deleted successfully"}
            handle_not_found("User not found")
        except InvalidId:
            handle_invalid_id("Invalid user ID format")
        except Exception as e:
            handle_error("Error deleting user", e)

    async def authenticate_user(self, email: str, password: str):
        try:
            user = self.collection.find_one({"email": email, "password": password})
            if user:
                token = self.create_jwt(user)
                return {"access_token": token}
            else:
                raise HTTPException(status_code=401, detail="Invalid email or password.")
        except HTTPException as e:
            raise e  
        except Exception as e:
            handle_error("Error during authentication", e)

    @staticmethod
    def create_jwt(user: dict) -> str:
        payload = {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
