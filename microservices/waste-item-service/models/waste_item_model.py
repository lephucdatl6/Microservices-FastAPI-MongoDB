from pydantic import BaseModel

class WasteItem(BaseModel):
    name: str
    material : str
    sorting_instructions: str
    score: int
    