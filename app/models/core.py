from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class Familia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    codigo_convite = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Monetização (preparado para o futuro)
    plano = db.Column(db.String(20), default='free')  # free, premium, vip
    data_expiracao = db.Column(db.DateTime, nullable=True)  # Quando expira o premium
    max_usuarios = db.Column(db.Integer, default=10)  # Limite de usuários (10 = ilimitado por enquanto)
    funcionalidades_premium = db.Column(db.Boolean, default=True)  # True = liberado para todos agora
    
    # Configurações personalizadas
    meta_reserva = db.Column(db.Float, default=40500.00)  # Meta de reserva de emergência personalizada

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(50), default='default.png')
    
    # Relacionamento com Familia
    familia = db.relationship('Familia', backref='usuarios', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
