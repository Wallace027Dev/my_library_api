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
        # Filtros de busca
        title = request.args.get('title')
        categories = request.args.get('categories')
        author = request.args.get('author')
        status_read = request.args.get('status_read')
        
        # Paginação e ordenação
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        order_by = request.args.get('order_by', default='title', type=str)
        direction = request.args.get('direction', default='asc', type=str)

        query = db.session.query(Book)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if categories:
            category_list = [cat.strip() for cat in categories.split(',')]
            for category in category_list:
                query = query.filter(Book.categories.ilike(f"%{category}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if status_read:
            query = query.filter(Book.status_read == status_read)
        
        # Ordenação segura
        if hasattr(Book, order_by):
            order_col = getattr(Book, order_by)
        else:
            order_col = Book.title
        
        # Ordenação
        if direction.lower() == 'desc':
            query = query.order_by(db.desc(order_col))
        else:
            query = query.order_by(order_col)
        
        # Paginação
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        books = pagination.items

        return jsonify(book_schema.dump(books, many=True)), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@books_bp.route('/<int:id>', methods=['PUT'])
def edit_book(id):
    try:
        data = request.get_json()
        print('Received data for editing book:', data)
        
        book = db.session.query(Book).get(id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        
        if 'title' in data:
            book.title = data['title']
        
        if 'author' in data:
            book.author = data['author']
        
        if 'img_url' in data:
            book.img_url = data['img_url']
        
        if 'categories' in data:
            categories = data['categories']
            if not isinstance(categories, list):
                return jsonify({"error": "Categories must be a list"}), 400
            book.categories_list = categories
        
        if 'status_read' in data:
            if data['status_read'] not in ['unread', 'reading', 'read']:
                return jsonify({"error": "Invalid status_read value"}), 400
            book.status_read = data['status_read']
        
        if 'rating' in data:
            book.rating = data['rating']
        
        db.session.commit()
        return jsonify(book_schema.dump(book)), 200 
        
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500