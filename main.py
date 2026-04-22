from fastapi import FastAPI
from database import engine
from models import Base
from routes import routes

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(routes.router)