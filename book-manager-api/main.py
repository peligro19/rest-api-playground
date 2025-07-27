from fastapi import FastAPI, HTTPException
from app.database import books_db
from app.models import Book, BookUpdate
from app.BookCRUD import BookCRUD

app = FastAPI(title="📚 Book Manager API")

# Home/Start Page
@app.get('/')
def home():
    return {"message": "Welcome to Book Manager API!"}

# Create New Book Entry
@app.post("/books/{book_id}")
def create_book(book_id: int, book: Book):
    created = BookCRUD.create_book(book_id, book)
    if not created:
        raise HTTPException(status_code=400, detail="Book already exists.")
    return created


# Get Specific Book by ID
@app.get("/books/{book_id}")
def read_book(book_id: int):
    book = BookCRUD.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book


### Get all Books
@app.get("/books")
def read_all_books():
    return BookCRUD.get_all_books() 


# Update Book Details by ID
@app.put("/books/{book_id}")
def update(book_id: int, book: BookUpdate):
    updated = BookCRUD.update_book(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found.")
    return updated


# Delete Book
@app.delete("/books/{book_id}")
def delete(book_id: int):
    deleted = BookCRUD.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found.")
    return {"message": "Book deleted successfully."}
