from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import User, UserCreate
from database import SessionLocal
from sqlalchemy.orm import Session
from models.user_model import User as DBUser

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(DBUser).filter(DBUser.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username is already taken!")
    
    new_user = DBUser(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=User)
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()

    if not db_user:  
        raise HTTPException(status_code=404, detail="User does not exist")
    
    if db_user.hashed_password != user.hashed_password:
        raise HTTPException(status_code=404, detail="Password is invalid")