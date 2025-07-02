from pydantic import BaseModel
from typing import Optional
from datetime import date


class Book(BaseModel):
    name: str
    title: str
    author: str
    pages: int
    publish_date: date