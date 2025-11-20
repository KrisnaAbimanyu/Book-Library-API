# Book Library API

System Integration Assignment 3, by Krisna Abimanyu — IS 2022

A simple RESTful API built using Flask that allows users to manage a collection of books.
This API supports full CRUD (Create, Read, Update, Delete) functionality, enabling users to retrieve book lists, add new books, update book details, and delete records easily.

## FEATURES
1. Retrieve all books
2. Retrieve a book by ID
3. Add a new book
4. Update book information
5. Delete a book record

## API ENDPOINTS (Method / Endpoint → Description)

- GET /api/books → Retrieve all book records
- GET /api/books/<id> → Retrieve a specific book by ID
- POST /api/books → Add a new book
- PUT /api/books/<id> → Update an existing book
- DELETE /api/books/<id> → Delete a book record

## SETUP INSTRUCTIONS

### 1. Clone the repository:
git clone <your_repo_url_here>
cd <repo_folder>
### 2 Install dependencies:
pip install flask
### 3 Run the app:
python app.py
### 4 The server runs at:
http://127.0.0.1:8000

## EXAMPLE API CALLS (via cURL)

### 1 Get all books:
curl -i http://127.0.0.1:8000/api/books
### 2 Add a new book:
curl -i -X POST -H "Content-Type: application/json"
-d '{"title": "Atomic Habits", "author": "James Clear"}'
http://127.0.0.1:8000/api/books
### 3 Update a book:
curl -i -X PUT -H "Content-Type: application/json"
-d '{"title": "Clean Code (Updated Edition)"}'
http://127.0.0.1:8000/api/books/2
### 4 Delete a book:
curl -i -X DELETE http://127.0.0.1:8000/api/books/1

## LIMITATIONS

- Data is stored in-memory; restarting the server resets all books.
- No authentication or access control implemented.
- This API is for educational purposes only, not production use.
