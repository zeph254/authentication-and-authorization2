from flask import Blueprint, jsonify, request
from models import Book, db
from datetime import datetime

book_bp = Blueprint('book_bp', __name__)

@book_bp.route("/books", methods=["POST"])
def add_books():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    publication_date = data.get("publication_date")

    if not title or not author or not publication_date:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert the publication_date string to a datetime.date object
        publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    check_title = Book.query.filter_by(title=title).first()
    if check_title:
        return jsonify({"error": "Book already exists"}), 400

    new_book = Book(title=title, author=author, publication_date=publication_date)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book saved successfully"}), 201

@book_bp.route("/books/<int:book_id>", methods=["PATCH"])
def update_books(book_id):
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    publication_date = data.get("publication_date")

    if not title or not author or not publication_date:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert the publication_date string to a datetime.date object
        publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book doesn't exist"}), 404

    # Check if the new title is already taken by another book
    check_title = Book.query.filter(Book.id != book_id, Book.title == title).first()
    if check_title:
        return jsonify({"error": "Book already exists"}), 400

    book.title = title
    book.author = author
    book.publication_date = publication_date
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

@book_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_books(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book doesn't exist"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200
