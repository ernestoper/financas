from flask import Flask
import os
from dotenv import load_dotenv
from app.extensions import db
from werkzeug.middleware.proxy_fix import ProxyFix

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def create_app(config_object=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuração (mantém compatibilidade)
    if config_object:
        app.config.from_object(config_object)
    else:
        # Configuração padrão (como estava antes)
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/financas.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar ProxyFix para Cloudflare/Reverse Proxy
    # x_for=1: confia no primeiro X-Forwarded-For
    # x_proto=1: confia no primeiro X-Forwarded-Proto
    # x_host=1: confia no primeiro X-Forwarded-Host
    # x_port=1: confia no primeiro X-Forwarded-Port
    # x_prefix=1: confia no primeiro X-Forwarded-Prefix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    
    # Configurar logs (opcional, só se logger.py existir)
    try:
        from logger import setup_logger, log_request
        setup_logger(app)
        log_request(app)
    except ImportError:
        pass  # Se não tiver logger, continua normal
    
    # Rate Limiting (opcional)
    try:
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["100 per hour"],
            storage_uri="memory://"
        )
    except ImportError:
        pass  # Se não tiver flask-limiter, continua normal
    
    # CORS
    try:
        from flask_cors import CORS
        CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    except ImportError:
        pass  # Se não tiver flask-cors, continua normal
    
    # Registrar Blueprints
    from app.routes import auth, main, api, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(admin.bp)
    
    
    # Criar tabelas se não existirem (apenas para dev)
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Endpoint para verificar se o sistema está funcionando"""
        return {
            'status': 'healthy',
            'service': 'Finanças Familiar',
            'version': '1.0.0'
        }, 200
    
    # Registrar error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        try:
            return render_template('errors/404.html'), 404
        except:
            return {'error': 'Página não encontrada'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        app.logger.error(f'Erro 500: {str(e)}')
        try:
            return render_template('errors/500.html'), 500
        except:
            return {'error': 'Erro interno do servidor'}, 500
        
    return app
