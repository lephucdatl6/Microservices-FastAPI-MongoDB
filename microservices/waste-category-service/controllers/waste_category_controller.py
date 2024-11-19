from fastapi import APIRouter, HTTPException
from models.waste_category_model import WasteCategory
from services.waste_category_service import WasteCategoryService

router = APIRouter()
category_service = WasteCategoryService()

@router.get("/")
async def get_categories():
    return await category_service.get_all_categories()

@router.post("/")
async def create_category(category: WasteCategory):
    return await category_service.create_category(category)

@router.get("/{category_id}")
async def get_category(category_id: str):
    return await category_service.get_category(category_id)

@router.put("/{category_id}")
async def update_category(category_id: str, category: WasteCategory):
    return await category_service.update_category(category_id, category)

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    return await category_service.delete_category(category_id)
