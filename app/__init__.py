import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
mi = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurações básicas para usar SQLite local
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///biblioteca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    
    # Inicializa as extensões
    db.init_app(app)
    ma.init_app(app)
    mi.init_app(app, db)
    
    # Registra Blueprints de rotas, exemplo futuro:
    from .routes.books import books_bp
    from .routes.wishlist import wishlist_bp
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

    return app
