from app import db
from app.models import Book, WishlistItem
from app.schemas import book_schema, wishlist_item_schema

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


books_bp = Blueprint('books', __name__)


@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    
    # Validação dos dados de entrada
    try:
        validated_data = book_schema.load(data)
    except ValidationError as err:
        return jsonify({ "errors": err.messages }), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    
    # Cria o objeto Book
    categories = validated_data.pop('categories')
    book = Book(**validated_data)
    book.categories_list = categories
    
    # Adiciona o novo livro ao banco de dados
    try:
        db.session.add(book)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    # Retorna o livro criado com status 201
    book_schema.context = {'obj': book}
    return jsonify(book_schema.dump(book)), 201


@books_bp.route('/', methods=['GET'])
def get_books():
    try:
        books = db.session.query(Book).all()
        
        for book in books:
            book_schema.context = {'obj': book}
        return jsonify(book_schema.dump(books, many=True)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
