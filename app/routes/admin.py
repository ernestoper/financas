from flask import Blueprint, render_template
from app.extensions import db
from app.models import User, Familia, Receita, DespesaFixa, DespesaVariavel, ReservaEmergencia
from app.utils import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_required
def admin_dashboard():
    # Estatísticas gerais
    total_familias = Familia.query.count()
    total_usuarios = User.query.count()
    
    # Famílias por plano
    familias_free = Familia.query.filter_by(plano='free').count()
    familias_premium = Familia.query.filter_by(plano='premium').count()
    familias_vip = Familia.query.filter_by(plano='vip').count()
    
    # Famílias recentes (últimas 10)
    familias_recentes = Familia.query.order_by(Familia.created_at.desc()).limit(10).all()
    
    # Estatísticas financeiras agregadas
    total_receitas = db.session.query(db.func.sum(Receita.valor)).filter(
        Receita.familia_id.in_([f.id for f in Familia.query.all()])
    ).scalar() or 0
    
    total_despesas_fixas = db.session.query(db.func.sum(DespesaFixa.valor)).filter(
        DespesaFixa.familia_id.in_([f.id for f in Familia.query.all()])
    ).scalar() or 0
    
    total_despesas_variaveis = db.session.query(db.func.sum(DespesaVariavel.valor)).filter(
        DespesaVariavel.familia_id.in_([f.id for f in Familia.query.all()])
    ).scalar() or 0
    
    total_reserva = db.session.query(db.func.sum(ReservaEmergencia.valor)).filter(
        ReservaEmergencia.familia_id.in_([f.id for f in Familia.query.all()])
    ).scalar() or 0
    
    # Usuários por família (média)
    usuarios_por_familia = total_usuarios / total_familias if total_familias > 0 else 0
    
    return render_template('admin.html',
        total_familias=total_familias,
        total_usuarios=total_usuarios,
        familias_free=familias_free,
        familias_premium=familias_premium,
        familias_vip=familias_vip,
        familias_recentes=familias_recentes,
        total_receitas=total_receitas,
        total_despesas_fixas=total_despesas_fixas,
        total_despesas_variaveis=total_despesas_variaveis,
        total_reserva=total_reserva,
        usuarios_por_familia=usuarios_por_familia
    )

@bp.route('/familias')
@admin_required
def admin_familias():
    familias = Familia.query.order_by(Familia.created_at.desc()).all()
    
    # Adicionar contagem de usuários para cada família
    familias_data = []
    for familia in familias:
        usuarios_count = User.query.filter_by(familia_id=familia.id).count()
        familias_data.append({
            'familia': familia,
            'usuarios_count': usuarios_count
        })
    
    return render_template('admin_familias.html', familias_data=familias_data)

@bp.route('/usuarios')
@admin_required
def admin_usuarios():
    usuarios = User.query.order_by(User.id.desc()).all()
    return render_template('admin_usuarios.html', usuarios=usuarios)
