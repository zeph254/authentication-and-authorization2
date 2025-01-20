from flask import Blueprint, jsonify, request
from models import Book, db
from datetime import datetime  # Import datetime for date conversion

book_bp = Blueprint('book_bp', __name__)

@book_bp.route("/books", methods=["POST"])
def add_books():
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    publication_date_str = data["publication_date"]  # Get date as string

    # Convert string to datetime object
    try:
        publication_date = datetime.strptime(publication_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    check_title = Book.query.filter_by(title=title).first()
    if check_title:
        return jsonify({"error": "Book already exists"}), 400
    else:
        new_book = Book(title=title, author=author, publication_date=publication_date)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book saved successfully"}), 201

@book_bp.route("/books<int:book_id>", methods=["PATCH"])
def update_books(book_id):
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    publication_date_str = data["publication_date"]

    # Convert string to datetime object
    try:
        publication_date = datetime.strptime(publication_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    book = Book.query.get(book_id)
    if book:
        check_title = Book.query.filter_by(title=title).first()
        if check_title:
            return jsonify({"error": "Book already exists"}), 400
        else:
            book.title = title
            book.author = author
            book.publication_date = publication_date
            db.session.commit()
            return jsonify({"message": "Book updated successfully"}), 200
    else:
        return jsonify({"error": "Book doesn't exist"}), 404

@book_bp.route("/books<int:book_id>", methods=["DELETE"])
def delete_books(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({"error": "Book doesn't exist"}), 404
