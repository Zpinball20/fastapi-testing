from pydantic import BaseModel

class ItemCreate(BaseModel):
    text: str
    is_done: bool = False

class Item(BaseModel):
    id: int
    text: str
    is_done: bool

    class Config:
        from_attributes = True