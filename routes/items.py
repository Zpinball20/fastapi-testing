from fastapi import APIRouter, HTTPException, Depends
from schemas.item_schema import Item, ItemCreate
from database import SessionLocal
from sqlalchemy.orm import Session
from models.item_model import Item as DBItem
from typing import Optional

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

@router.get("/items/", response_model=list[Item])
def filter_items(done: Optional[bool] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(DBItem)

    if done is not None:
        query = query.filter(DBItem.is_done == done)
        
    query = query.offset(skip).limit(limit)

    return query.all()

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
    
    new_item = DBItem(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
    

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.text = item.text
    db_item.is_done = item.is_done

    db.commit()
    db.refresh(db_item)

    return db_item

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()

    return {"message" : "Item successfully deleted"}