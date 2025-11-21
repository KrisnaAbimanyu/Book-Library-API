from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory "database"
books = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"}
]


def get_next_id():
    """Get the next book ID."""
    if not books:
        return 1
    return max(book["id"] for book in books) + 1


#GET /api/books  -> get all books
@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


#GET /api/books/<id>  -> get one book by id
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book), 200


#POST /api/books  -> add a new book
@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({"error": "Both 'title' and 'author' are required"}), 400

    new_book = {
        "id": get_next_id(),
        "title": title,
        "author": author
    }
    books.append(new_book)
    return jsonify(new_book), 201


#PUT /api/books/<id>  -> update a book
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # Allow partial update (if title not sent, keep old title, etc.)
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])

    return jsonify(book), 200


#DELETE /api/books/<id>  -> delete a book
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")

    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    # Run on port 8000 so it matches your README examples
    app.run(debug=True, port=8000)
