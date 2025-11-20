from app import db
from app.models import WishlistItem
from app.schemas import wishlist_item_schema

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route('/', methods=['POST'])
def create_wishlist_item():
    data = request.get_json()
    
    # Validação dos dados de entrada
    try:
        validated_data = wishlist_item_schema.load(data)
    except ValidationError as err:
        return jsonify({ "errors": err.messages }), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    
    # Cria o objeto WishlistItem
    categories = validated_data.pop('categories')
    wishlist_item = WishlistItem(**validated_data)
    wishlist_item.categories_list = categories
    
    # Adiciona o novo item à wishlist no banco de dados
    try:
        db.session.add(wishlist_item)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    # Retorna o item criado com status 201
    return jsonify(wishlist_item_schema.dump(wishlist_item)), 201


@wishlist_bp.route('/', methods=['GET'])
def get_wishlist_items():
    try:
        # Filtros de busca
        title = request.args.get('title')
        categories = request.args.get('categories')
        author = request.args.get('author')
        
        # Paginação e ordenação
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        order_by = request.args.get('order_by', default='title', type=str)
        direction = request.args.get('direction', default='asc', type=str)

        query = db.session.query(WishlistItem)
        if title:
            query = query.filter(WishlistItem.title.ilike(f"%{title}%"))
        if categories:
            category_list = [cat.strip() for cat in categories.split(',')]
            for category in category_list:
                query = query.filter(WishlistItem.categories.ilike(f"%{category}%"))
        if author:
            query = query.filter(WishlistItem.author.ilike(f"%{author}%"))
        
        # Ordenação segura
        if hasattr(WishlistItem, order_by):
            order_col = getattr(WishlistItem, order_by)
        else:
            order_col = WishlistItem.title
        
        # Ordenação
        if direction.lower() == 'desc':
            query = query.order_by(db.desc(order_col))
        else:
            query = query.order_by(order_col)
        
        # Paginação
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        wishlist_items = pagination.items

        return jsonify(wishlist_item_schema.dump(wishlist_items, many=True)), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# @books_bp.route('/<int:id>', methods=['DELETE'])
# def delete_book(id):
#     try:
#         book = db.session.query(Book).get(id)
#         if not book:
#             return jsonify({"error": "Book not found"}), 404
        
#         db.session.delete(book)
#         db.session.commit()
#         return jsonify({"message": "Book deleted successfully"}), 200

#     except SQLAlchemyError as e:
#         return jsonify({"error": str(e)}), 500
