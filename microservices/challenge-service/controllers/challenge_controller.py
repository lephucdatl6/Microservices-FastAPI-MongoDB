from fastapi import APIRouter, HTTPException
from models.challenge_model import Challenge
from services.challenge_service import ChallengeService

router = APIRouter()
challenge_service = ChallengeService()

@router.get("/")
async def get_challenges():
    return await challenge_service.get_all_challenges()

@router.post("/")
async def create_challenge(challenge: Challenge):
    return await challenge_service.create_challenge(challenge)

@router.get("/{challenge_id}")
async def get_challenge(challenge_id: str):
    return await challenge_service.get_challenge(challenge_id)

@router.put("/{challenge_id}")
async def update_challenge(challenge_id: str, challenge: Challenge):
    return await challenge_service.update_challenge(challenge_id, challenge)

@router.delete("/{challenge_id}")
async def delete_challenge(challenge_id: str):
    return await challenge_service.delete_challenge(challenge_id)
