from pydantic import BaseModel

class WasteCategory(BaseModel):
    name: str
    description: str