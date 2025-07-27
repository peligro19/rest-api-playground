from pydantic import BaseModel
from typing import Optional
from datetime import date


class Book(BaseModel):
    name: str
    title: str
    author: str
    pages: int
    publish_date: date


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None