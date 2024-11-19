from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import User
from services.user_service import UserService
from middleware.auth_middleware import JWTBearer

router = APIRouter()
user_service = UserService()

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await user_service.authenticate_user(form_data.username, form_data.password)

@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_users():
    return await user_service.get_all_users()

# @router.get("/")
# async def get_users():
#     return await user_service.get_all_users()

@router.post("/")
async def create_user(user: User):
    return await user_service.create_user(user)

@router.get("/{user_id}")
async def get_user(user_id: str):
    return await user_service.get_user(user_id)

@router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    return await user_service.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return await user_service.delete_user(user_id)


