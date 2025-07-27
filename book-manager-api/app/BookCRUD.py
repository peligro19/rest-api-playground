from app.models import Book, BookUpdate
from app.database import books_db

class BookCRUD:
    @staticmethod
    def create_book(book_id: int, book: Book):
        if book_id in books_db:
            return None
        books_db[book_id] = book
        return book
    
    @staticmethod
    def get_book(book_id: int):
        return books_db.get(book_id)
    
    @staticmethod
    def get_all_books():
        return list(books_db.values())
    
    @staticmethod
    def update_book(book_id: int, book_data: BookUpdate):
        if book_id not in books_db:
            return None
        stored_book = books_db[book_id]
        updated_data = book_data.dict(exclude_unset=True)
        updated_book = stored_book.copy(update=updated_data)
        books_db[book_id] = updated_book
        return updated_book

    @staticmethod
    def delete_book(book_id: int):
        return books_db.pop(book_id, None)
