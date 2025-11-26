"""
Configurações do Sistema de Finanças Familiar
"""
import os
from dotenv import load_dotenv
import secrets

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações base"""
    
    # Chave secreta
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    
    # Banco de dados (local)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///instance/financas.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    RATELIMIT_STORAGE_URL = 'memory://'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Sessão
    SESSION_COOKIE_SECURE = True  # Cookies apenas em HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    FLASK_ENV = 'production'

# Selecionar configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

def get_config():
    """Retorna a configuração apropriada"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
