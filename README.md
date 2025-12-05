# Book Library API — System Integration Assignment 4

By Krisna Abimanyu — IS 2022

A secure RESTful API built using Flask, featuring User Authentication, JWT-based Authorization, and Persistent JSON Storage.
Users must register and log in to obtain a JWT token before they can create, update, or delete books.

This API provides:

User Registration & Login

JWT Access Token generation

Protected routes requiring authentication

Owner-based Authorization

Persistent storage using users.json and books.json

-------------------------------------------------------
FEATURES
-------------------------------------------------------
🔐 Authentication

Register new users

Login using username + password

Receive JWT token for protected endpoints

📚 Books Management

Retrieve all books (public)

Retrieve a book by ID (public)

Add a new book (auth required)

Update a book (owner only)

Delete a book (owner only)

💾 Persistent Storage

users.json → stores usernames + hashed passwords

books.json → stores all books

Data remains saved even after app restart

-------------------------------------------------------
API ENDPOINTS
-------------------------------------------------------
🔐 AUTHENTICATION
POST /register

Register a new user
Body:

{ "username": "krisna", "password": "1234" }

POST /login

Login and receive JWT token
Body:

{ "username": "krisna", "password": "1234" }


Response Example:

{ "access_token": "<JWT_TOKEN>" }

🔸 All Protected Endpoints Require:
Authorization: Bearer <JWT_TOKEN>

📚 BOOKS API
GET /api/books

Retrieve all books (public)

GET /api/books/<id>

Retrieve a book by ID (public)

POST /api/books

Add a new book (authentication required)

Headers:

Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json


Body:

{ "title": "New Book", "author": "Krisna" }

PUT /api/books/<id>

Update book info (owner only)

DELETE /api/books/<id>

Delete a book (owner only)

-------------------------------------------------------
SETUP INSTRUCTIONS
-------------------------------------------------------
1. Clone the repository
git clone <your_repo_url>
cd <repo_folder>

2. Install dependencies
pip install Flask Flask-JWT-Extended Werkzeug


Or using requirements.txt:

pip install -r requirements.txt

3. Run the app
python app.py

4. Server URL
http://127.0.0.1:8000

-------------------------------------------------------
EXAMPLE API CALLS (cURL)
-------------------------------------------------------
✔ Register a user
curl -X POST -H "Content-Type: application/json" \
-d "{\"username\": \"krisna\", \"password\": \"1234\"}" \
http://127.0.0.1:8000/register

✔ Login and receive token
curl -X POST -H "Content-Type: application/json" \
-d "{\"username\": \"krisna\", \"password\": \"1234\"}" \
http://127.0.0.1:8000/login

✔ Get all books
curl http://127.0.0.1:8000/api/books

✔ Add a new book
curl -X POST -H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d "{\"title\": \"Atomic Habits\", \"author\": \"James Clear\"}" \
http://127.0.0.1:8000/api/books

-------------------------------------------------------
LIMITATIONS
-------------------------------------------------------

Data stored in JSON files (not a real database)

JWT secret key not secure for production

Intended for educational use only
