from flask import Flask
import os
from dotenv import load_dotenv
from app.extensions import db

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuração
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///financas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar Blueprints
    from app.routes import auth, main, api, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(admin.bp)
    
    # Criar tabelas se não existirem (apenas para dev)
    with app.app_context():
        db.create_all()
        
    return app
