import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    # Configurações básicas para usar SQLite local
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///biblioteca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    
    # Inicializa as extensões
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    # Importa modelos para garantir registro com o sqlalchemy
    from . import models
    
    # (Opcional) registra Blueprints de rotas, exemplo futuro:
    # from .routes.livros import livros_bp
    # app.register_blueprint(livros_bp)

    return app
