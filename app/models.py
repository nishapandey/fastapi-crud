from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)


class PostCreate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True
