from flask import Blueprint, render_template, redirect, url_for, session
from app.models import Familia
from app.utils import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    familia = Familia.query.get(session.get('familia_id'))
    return render_template('dashboard.html', meta_reserva=familia.meta_reserva if familia else 40500.00)

@bp.route('/receitas')
@login_required
def receitas_page():
    return render_template('receitas.html')

@bp.route('/despesas-fixas')
@login_required
def despesas_fixas_page():
    return render_template('despesas_fixas.html')

@bp.route('/despesas-variaveis')
@login_required
def despesas_variaveis_page():
    return render_template('despesas_variaveis.html')

@bp.route('/reserva')
@login_required
def reserva_page():
    familia = Familia.query.get(session.get('familia_id'))
    return render_template('reserva.html', meta_reserva=familia.meta_reserva if familia else 40500.00)

@bp.route('/planos')
@login_required
def planos():
    return render_template('planos.html')

@bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', meta_reserva=0) # Placeholder, will be fetched via API

@bp.route('/metas')
@login_required
def metas():
    return render_template('metas.html', meta_reserva=0) # Placeholder, will be fetched via API
