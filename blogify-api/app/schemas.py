from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr


class BlogCreate(BaseModel):
    title: str
    content: str
    author_id: int


class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
