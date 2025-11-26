from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import User, Familia
import secrets

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'criar_familia':
            # Criar nova família
            nome_familia = request.form.get('nome_familia')
            username = request.form.get('username')
            nome_usuario = request.form.get('nome_usuario')
            password = request.form.get('password')
            
            # Gerar código de convite único
            codigo_convite = secrets.token_urlsafe(8)
            
            familia = Familia(
                nome=nome_familia, 
                codigo_convite=codigo_convite,
                meta_reserva=40500.00  # Meta padrão
            )
            db.session.add(familia)
            db.session.flush()
            
            # Apenas o primeiro usuário (ernesto) é admin do sistema
            user = User(username=username, nome=nome_usuario, familia_id=familia.id, is_admin=False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['nome'] = user.nome
            session['familia_id'] = user.familia_id
            session['codigo_convite'] = codigo_convite
            session['is_admin'] = user.is_admin
            
            return redirect(url_for('main.dashboard'))
        
        elif action == 'entrar_familia':
            # Entrar em família existente
            codigo_convite = request.form.get('codigo_convite')
            username = request.form.get('username')
            nome_usuario = request.form.get('nome_usuario')
            password = request.form.get('password')
            
            familia = Familia.query.filter_by(codigo_convite=codigo_convite).first()
            if not familia:
                return render_template('register.html', error='Código de convite inválido')
            
            user = User(username=username, nome=nome_usuario, familia_id=familia.id, is_admin=False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['nome'] = user.nome
            session['familia_id'] = user.familia_id
            session['is_admin'] = user.is_admin
            
            return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['nome'] = user.nome
            session['familia_id'] = user.familia_id
            session['is_admin'] = user.is_admin
            
            # Pegar código de convite se for admin
            if user.is_admin:
                familia = Familia.query.get(user.familia_id)
                session['codigo_convite'] = familia.codigo_convite
            
            return redirect(url_for('main.dashboard'))
        
        return render_template('login.html', error='Usuário ou senha inválidos')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
