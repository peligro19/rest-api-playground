# 📚 Book Manager API

A simple and beginner-friendly **CRUD API using FastAPI** to manage a collection of books. This version uses an **in-memory dictionary** for storage and organizes CRUD logic inside a class for better code structure.

---

## 🚀 Features

- 📖 Add a new book
- 📚 Get all books
- 🔍 Get a book by ID
- ✏️ Update book details
- ❌ Delete a book
- 🧼 Clean, modular code (CRUD in class)
- 🧪 Swagger & ReDoc UI documentation

---

## 📁 Project Structure

```
book_manager/
│
├── main.py                  # Entry point of the FastAPI application
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignored files
│
└── app/                     # Application package
    ├── __init__.py          # Makes 'app' a Python package (optional but good practice)
    ├── models.py            # Pydantic models (Book, BookUpdate)
    ├── database.py          # In-memory database (books_db dictionary)
    ├── crud.py              # Class-based CRUD logic (BookCRUD)
```

---

## 🧰 Requirements

- Python 3.7+
  - `pip install python`
- FastAPI
  - `pip install fastapi`
- Uvicorn
  - `pip install uvicorn`

---

## ⚙️ Installation & Running the API

1. **Clone the project**

```bash
git clone https://github.com/your-username/book-manager-api.git
cd book-manager-api
```

2. **Install dependencies**

```bash
pip install -r ./requirements.txt
```

3. **Run the server**

```bash
uvicorn main:app --reload
```

4. **Visit API docs**

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Common HTTP Path Decorators:

https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods

| Method   | Decorator        | Usage Example             |
|----------|------------------|---------------------------|
| POST     | `@app.post()`    | Create resource           |
| GET      | `@app.get()`     | Read/Fetch data           |
| PUT      | `@app.put()`     | Update resource           |
| DELETE   | `@app.delete()`  | Delete resource           |

---

## 📦 Example API Usage

### 🔸 Create a Book

`POST /books/1`

```json
{
  "title": "FastAPI for Beginners",
  "author": "Sumit Kumar",
  "pages": 200
}
```

### 🔸 Get All Books

`GET /books/`

### 🔸 Get a Single Book

`GET /books/1`

### 🔸 Update Book Details

`PUT /books/1`

```json
{
  "pages": 250
}
```

### 🔸 Delete a Book

`DELETE /books/1`

---

## 📌 Tech Stack

- ⚡ FastAPI
- 🧠 Pydantic
- 🐍 Python 3
- 🧪 Swagger/OpenAPI (auto-generated)

---

## 📈 Next Steps

Want to extend this project?

- 🔗 Add SQLite/PostgreSQL database
- 🧵 Use SQLAlchemy or SQLModel for ORM
- 🔐 Add authentication (JWT)
- 📦 Containerize with Docker

---

## 🤝 Contributing

This project is meant for **learning purposes**. Feel free to fork, clone, or extend it as per your need. Contributions and suggestions are welcome!

---

## 🧾 License

MIT License
