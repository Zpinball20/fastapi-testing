from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int = None
    text: str = None
    is_done: bool = False

items = []
next_id = 0

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/items")
def create_item(item: Item):
    global next_id
    item.id = next_id
    next_id += 1
    items.append(item)
    return item

@app.get("/items", response_model = list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            item.id = item_id
            items[index] = item
            return item
    
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    for item_obj in items:
        if item_obj.id == item_id:
            return item_obj
    
    raise HTTPException(status_code= 404, detail="Item Not Found")
    

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for item_obj in items:
        if item_obj.id == item_id:
            items.remove(item_obj)
            return {"message": "Item deleted"}
    
    raise HTTPException(status_code=404, detail="Item not found")