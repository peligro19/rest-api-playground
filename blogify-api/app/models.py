from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int = Field(foreign_key="user.id")

    # ✅ Define relationship to User (author)
    author: Optional["User"] = Relationship(back_populates="blogs")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str

    # ✅ Define relationship to Blog
    blogs: List[Blog] = Relationship(back_populates="author")


# Needed when using forward references (strings in type hints)
Blog.model_rebuild()
User.model_rebuild()