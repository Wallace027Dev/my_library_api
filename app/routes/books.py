from flask import Blueprint, jsonify, request
from app import db
from app.models import Book, WishlistItem
from app.schemas import book_schema, wishlist_item_schema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    
    # Validação e desserialização dos dados de entrada
    try:
        book = book_schema.load(data)
    except ValidationError as err:
        return jsonify({ "errors": err.messages }), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    
    # Adiciona o novo livro ao banco de dados
    try:
        db.session.add(book)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    # Retorna o livro criado com status 201
    return book_schema.jsonify(book), 201
