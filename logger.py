"""
Sistema de Logs com Rotação
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(app):
    """Configura o sistema de logs"""
    
    # Criar diretório de logs se não existir
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
    except PermissionError:
        # Se não tiver permissão (Docker), usar /tmp
        app.config['LOG_FILE'] = '/tmp/app.log'
    
    # Configurar nível de log
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    
    # Formato dos logs
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo com rotação (10MB, manter 10 arquivos)
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Adicionar handlers ao app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Log de inicialização
    app.logger.info('='*50)
    app.logger.info('Sistema de Finanças Familiar iniciado')
    app.logger.info(f'Ambiente: {app.config["FLASK_ENV"]}')
    app.logger.info(f'Debug: {app.config["DEBUG"]}')
    app.logger.info(f'Host: {app.config["HOST"]}:{app.config["PORT"]}')
    app.logger.info('='*50)
    
    return app.logger

def log_request(app):
    """Middleware para logar requisições"""
    @app.before_request
    def before_request():
        from flask import request
        app.logger.debug(f'{request.method} {request.path} - {request.remote_addr}')
    
    @app.after_request
    def after_request(response):
        from flask import request
        app.logger.debug(f'{request.method} {request.path} - {response.status_code}')
        return response

def log_error(app):
    """Handler para erros"""
    @app.errorhandler(Exception)
    def handle_exception(e):
        from flask import request
        app.logger.error(f'Erro não tratado: {str(e)}')
        app.logger.error(f'URL: {request.url}')
        app.logger.error(f'Método: {request.method}')
        app.logger.error(f'IP: {request.remote_addr}')
        app.logger.exception(e)
        
        # Re-raise para o Flask tratar
        raise e
