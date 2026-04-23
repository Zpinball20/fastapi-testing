from database import Base
from sqlalchemy import String, Column, Integer, Boolean, DateTime
from datetime import datetime, timezone

class Item(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False, unique=True)
    is_done = Column(Boolean, nullable=False)
    created_at = Column(DateTime, 
                        default=lambda: datetime.now(timezone.utc), 
                        nullable=False
    )
    
    updated_at = Column(DateTime, 
                        default=lambda: datetime.now(timezone.utc), 
                        onupdate=lambda: datetime.now(timezone.utc)
    )