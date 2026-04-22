from fastapi import FastAPI
from database import items
#import ./routes/routes.py

app = FastAPI()

app.include_router(items.router)