from fastapi import FastAPI, HTTPException
from app.database import books_db
from app.models import Book

app = FastAPI()

# Home/Start Page
@app.get('/')
def home():
    return {"message": "Welcome to Book Manager API!"}

# Create New Book Entry
@app.post("/books/{book_id}")
def create_book(book_id: int, book: Book):
    if not books_db.get(book_id):
        books_db[book_id] = book
    return book
