from fastapi import APIRouter, HTTPException
from models.waste_item_model import WasteItem
from services.waste_item_service import WasteItemService

router = APIRouter()
item_service = WasteItemService()


@router.get("/")
async def get_items():
    return await item_service.get_all_items()

@router.post("/")
async def create_item(item: WasteItem):
    return await item_service.create_item(item)

@router.get("/{item_id}")
async def get_item(item_id: str):
    return await item_service.get_item(item_id)

@router.put("/{item_id}")
async def update_item(item_id: str, item: WasteItem):
    return await item_service.update_item(item_id, item)

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    return await item_service.delete_item(item_id)

