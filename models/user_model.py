from database import Base
from sqlalchemy import String, Column, Integer, DateTime
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    created_at = Column(DateTime, 
                        default=lambda: datetime.now(timezone.utc), 
                        nullable=False
    )
    
    updated_at = Column(DateTime, 
                        default=lambda: datetime.now(timezone.utc), 
                        onupdate=lambda: datetime.now(timezone.utc)
    )