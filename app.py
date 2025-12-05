from flask import Flask, jsonify, request, abort
import os
import json
import datetime

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =======================
# JWT CONFIGURATION
# =======================
# In a real app, use a long random secret and keep it private
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

jwt = JWTManager(app)

# =======================
# FILE PATHS (PERSISTENT STORAGE)
# =======================

USERS_FILE = "users.json"
BOOKS_FILE = "books.json"


# =======================
# USERS "DATABASE" (PERSISTENT)
# =======================

def load_users():
    """Load users from users.json. Returns a dict: {username: {password_hash: ...}}"""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users):
    """Save users dict back to users.json."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


# =======================
# BOOKS "DATABASE" (PERSISTENT)
# =======================

def load_books():
    """Load books from books.json. Returns a list of books."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_books(books_list):
    """Save books list back to books.json."""
    with open(BOOKS_FILE, "w") as f:
        json.dump(books_list, f, indent=2)


# Note: owner will store the username who created the book
books = load_books()

# Seed default books if none exist yet
if not books:
    books = [
        {
            "id": 1,
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "owner": None,  # seeded book, no owner
        },
        {
            "id": 2,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "owner": None,  # seeded book, no owner
        },
    ]
    save_books(books)


def get_next_id():
    """Get the next book ID."""
    if not books:
        return 1
    return max(book["id"] for book in books) + 1


# =======================
# AUTHENTICATION ENDPOINTS
# =======================

@app.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Body JSON: {"username": "...", "password": "..."}
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    users = load_users()

    if username in users:
        return jsonify({"error": "username already exists"}), 400

    # Hash the password before saving
    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    users[username] = {
        "password_hash": password_hash
    }

    save_users(users)

    return jsonify({"message": "user registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Log in an existing user.
    Body JSON: {"username": "...", "password": "..."}
    Returns: {"access_token": "..."}
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    users = load_users()
    user = users.get(username)

    if not user:
        return jsonify({"error": "invalid username or password"}), 401

    password_hash = user.get("password_hash")
    if not check_password_hash(password_hash, password):
        return jsonify({"error": "invalid username or password"}), 401

    # Create JWT token with the username as identity
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200


# =======================
# BOOKS API
# =======================

# GET /api/books  -> get all books (public)
@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


# GET /api/books/<id>  -> get one book by id (public)
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book), 200


# POST /api/books  -> add a new book (AUTH REQUIRED)
@app.route("/api/books", methods=["POST"])
@jwt_required()
def create_book():
    """
    Create a new book.
    Only logged-in users can create books.
    The book will be owned by the current user.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({"error": "Both 'title' and 'author' are required"}), 400

    current_user = get_jwt_identity()

    new_book = {
        "id": get_next_id(),
        "title": title,
        "author": author,
        "owner": current_user,  # owner = username from the token
    }
    books.append(new_book)
    save_books(books)

    return jsonify(new_book), 201


# PUT /api/books/<id>  -> update a book (AUTH + OWNER ONLY)
@app.route("/api/books/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")

    current_user = get_jwt_identity()

    # Only the owner can modify the book
    if book.get("owner") != current_user:
        return jsonify({"error": "you are not allowed to modify this book"}), 403

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # Allow partial update (if title not sent, keep old title, etc.)
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])

    save_books(books)
    return jsonify(book), 200


# DELETE /api/books/<id>  -> delete a book (AUTH + OWNER ONLY)
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")

    current_user = get_jwt_identity()

    # Only the owner can delete the book
    if book.get("owner") != current_user:
        return jsonify({"error": "you are not allowed to delete this book"}), 403

    books = [b for b in books if b["id"] != book_id]
    save_books(books)

    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    # Run on port 8000 so it matches your README examples
    app.run(debug=True, port=8000)
