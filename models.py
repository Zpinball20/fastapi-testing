from database import Base
from sqlalchemy import String, Column, Integer

class Items(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False, unique=True)
    is_done = Column(bool, nullable=False)