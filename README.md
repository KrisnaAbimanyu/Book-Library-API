Book Library API — System Integration Assignment 4  
By Krisna Abimanyu — IS 2022

A secure RESTful API built using Flask that allows users to manage a library of books with Authentication, Authorization, and persistent JSON storage. Users must register and log in to obtain a JWT token before creating, updating, or deleting books.

This API includes:
- User Registration
- User Login (JWT access token)
- Protected routes using JWT
- Owner-based Authorization
- Persistent data storage using users.json and books.json

-------------------------------------------------------
FEATURES
-------------------------------------------------------
Authentication:
- Register new users
- Login and receive a JWT token

Books Management:
1. Retrieve all books (public)
2. Retrieve a book by ID (public)
3. Add a new book (auth required)
4. Update a book (owner only)
5. Delete a book (owner only)

Persistent Storage:
- users.json stores hashed passwords
- books.json stores book records
- Data stays saved even after server restart

-------------------------------------------------------
API ENDPOINTS
-------------------------------------------------------

AUTHENTICATION
POST /register  
Body:
{ "username": "krisna", "password": "1234" }

POST /login  
Body:
{ "username": "krisna", "password": "1234" }

Response:
{ "access_token": "<JWT_TOKEN>" }

All protected endpoints require:
Authorization: Bearer <JWT_TOKEN>

-------------------------------------------------------

BOOKS API

GET /api/books
Retrieve all books (public)

GET /api/books/<id>
Retrieve a book by ID (public)

POST /api/books
Add a new book (auth required)
Headers:
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Body:
{ "title": "New Book", "author": "Krisna" }

PUT /api/books/<id>
Update an existing book (owner only)

DELETE /api/books/<id>
Delete a book (owner only)

-------------------------------------------------------
SETUP INSTRUCTIONS
-------------------------------------------------------

1. Clone the repository:
git clone <your_repo_url_here>
cd <repo_folder>

2. Install dependencies:
pip install Flask Flask-JWT-Extended Werkzeug

(Or using requirements.txt)
pip install -r requirements.txt

3. Run the app:
python app.py

4. The server runs at:
http://127.0.0.1:8000

-------------------------------------------------------
EXAMPLE API CALLS (cURL)
-------------------------------------------------------

Register user:
curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"krisna\", \"password\": \"1234\"}" http://127.0.0.1:8000/register

Login user:
curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"krisna\", \"password\": \"1234\"}" http://127.0.0.1:8000/login

Get all books:
curl http://127.0.0.1:8000/api/books

Add a new book:
curl -X POST -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"title\": \"Atomic Habits\", \"author\": \"James Clear\"}" http://127.0.0.1:8000/api/books

-------------------------------------------------------
LIMITATIONS
-------------------------------------------------------
- Data is stored in JSON files (not a real database)
- JWT secret key is not production secure
- Not suitable for production without modifications

-------------------------------------------------------
END OF README
-------------------------------------------------------
