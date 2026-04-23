from fastapi import APIRouter, HTTPException, Depends
from schemas import Item, ItemCreate
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Item as DBItem

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message" : "Task Manager App Test"}

@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, db:Session = Depends(get_db)) -> Item:
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@router.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db:Session = Depends(get_db)):
    if db.query(DBItem).filter(DBItem.text == item.text).first():
        raise HTTPException(status_code=409, detail="Task already exists!")
    
    newItem = DBItem(**item.model_dump())
    db.add(newItem)
    db.commit()
    db.refresh(newItem)
    return newItem
    

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            item.id = item_id
            items[index] = item
            return item
    
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    for item_obj in items:
        if item_obj.id == item_id:
            items.remove(item_obj)
            return {"message": "Item deleted"}
    
    raise HTTPException(status_code=404, detail="Item not found")