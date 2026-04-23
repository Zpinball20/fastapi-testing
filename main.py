from fastapi import FastAPI
from database import engine
from models.item_model import Base
from routes import items

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(items.router)