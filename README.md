Book Library API
System Integration — Assignment 4
Author: Krisna Abimanyu (IS 2022)

A secure and lightweight RESTful API built using Flask, featuring JWT authentication, owner-based authorization, and persistent JSON storage.

METHOD OVERVIEW
1. Authentication Layer (register → login → token)
2. Authorization Rules (only owners can modify/delete)
3. Persistent Storage (users.json & books.json)
4. REST API Structure (/api/books)

DEPENDENCIES
Flask
Flask-JWT-Extended
Werkzeug

Install:
pip install Flask Flask-JWT-Extended Werkzeug

SETUP
git clone <repo_url>
cd <repo_folder>
python app.py

BASE URL
http://127.0.0.1:8000

AUTHENTICATION ENDPOINTS
POST /register
POST /login

BOOK ENDPOINTS
GET /api/books
GET /api/books/<id>
POST /api/books   (JWT required)
PUT /api/books/<id>   (Owner only)
DELETE /api/books/<id>   (Owner only)

CURL EXAMPLES
Register:
curl -X POST -H "Content-Type: application/json" -d "{"username":"krisna","password":"1234"}" http://127.0.0.1:8000/register

Login:
curl -X POST -H "Content-Type: application/json" -d "{"username":"krisna","password":"1234"}" http://127.0.0.1:8000/login

Get all books:
curl http://127.0.0.1:8000/api/books

Add book:
curl -X POST -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{"title":"Atomic Habits","author":"James Clear"}" http://127.0.0.1:8000/api/books

Update book:
curl -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{"title":"Updated Version"}" http://127.0.0.1:8000/api/books/3

Delete book:
curl -X DELETE -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/api/books/3

TROUBLESHOOTING
401 → Missing or expired token
403 → Not the owner of the book
JSON not updating → Ensure save_books() runs

LIMITATIONS
Not a production database
Simple JWT setup
No refresh tokens
