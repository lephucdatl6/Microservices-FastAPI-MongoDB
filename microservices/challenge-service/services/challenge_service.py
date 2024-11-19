from middleware.error_handler import handle_error, handle_invalid_id, handle_not_found
from aiocache import Cache, cached
from bson import ObjectId
from bson.errors import InvalidId
import pymongo
import os

class ChallengeService:
    def __init__(self):
        try:
            client = pymongo.MongoClient(os.getenv("MONGO_URL"))
            self.db = client[os.getenv("DATABASE_NAME")]
            self.collection = self.db["challenges"]
            self.cache = Cache.from_url("memory://")
        except Exception as e:
            handle_error("Database connection error", e)

    async def get_all_challenges(self):
        try:
            cached_challenges = await self.cache.get("all_challenges")
            if cached_challenges:
                return cached_challenges
            challenges = list(self.collection.find())
            await self.cache.set("all_challenges", [{**challenge, "_id": str(challenge["_id"])} for challenge in challenges], ttl=60)
            return [{**challenge, "_id": str(challenge["_id"])} for challenge in challenges]
        except Exception as e:
            handle_error("Error fetching challenges", e)

    async def create_challenge(self, challenge):
        try:
            challenge_data = challenge.dict()
            result = self.collection.insert_one(challenge_data)
            challenge_data["_id"] = str(result.inserted_id)
            await self.cache.delete("all_challenges")
            return challenge_data
        except Exception as e:
            handle_error("Error creating challenge", e)

    async def get_challenge(self, challenge_id):
        try:
            challenge = self.collection.find_one({"_id": ObjectId(challenge_id)})
            if challenge:
                return {**challenge, "_id": str(challenge["_id"])}
            handle_not_found("Challenge not found")
        except InvalidId:
            handle_invalid_id("Invalid challenge ID format")
        except Exception as e:
            handle_error("Error fetching challenge", e)

    async def update_challenge(self, challenge_id, challenge):
        try:
            result = self.collection.update_one({"_id": ObjectId(challenge_id)}, {"$set": challenge.dict()})
            if result.modified_count == 1:
                await self.cache.delete("all_challenges")
                return {"message": "Challenge updated successfully"}
            handle_not_found("Challenge not found")
        except InvalidId:
            handle_invalid_id("Invalid challenge ID format")
        except Exception as e:
            handle_error("Error updating challenge", e)

    async def delete_challenge(self, challenge_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(challenge_id)})
            if result.deleted_count == 1:
                await self.cache.delete("all_challenges")
                return {"message": "Challenge deleted successfully"}
            handle_not_found("Challenge not found")
        except InvalidId:
            handle_invalid_id("Invalid challenge ID format")
        except Exception as e:
            handle_error("Error deleting challenge", e)
