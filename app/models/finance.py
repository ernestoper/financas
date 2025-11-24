from app.extensions import db

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)  # 2025, 2026...
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)

class DespesaFixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    pago = db.Column(db.Boolean, default=False)
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)  # 2025, 2026...
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Quem criou
    pago_por_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Quem pagou
    data_pagamento = db.Column(db.DateTime, nullable=True)  # Quando foi pago
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)
    
    # Recorrência
    recorrente = db.Column(db.Boolean, default=False)
    dia_vencimento = db.Column(db.Integer, nullable=True)

class DespesaVariavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)

class ReservaGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor_meta = db.Column(db.Float, nullable=False)
    cor = db.Column(db.String(20), default='#4CAF50')
    icone = db.Column(db.String(50), default='fas fa-piggy-bank')
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)

class ReservaEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('reserva_goal.id'), nullable=True)

class MetaCategoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    valor_limite = db.Column(db.Float, nullable=False)
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)
