from pydantic import BaseModel

class Item(BaseModel):
    id: int = None
    text: str = None
    is_done: bool = False