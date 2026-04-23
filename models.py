from database import Base
from sqlalchemy import String, Column, Integer, Boolean

class Item(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False, unique=True)
    is_done = Column(Boolean, nullable=False)