from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
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
    
    # Relacionamento com Familia
    familia = db.relationship('Familia', backref='usuarios', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

class DespesaVariavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)

class ReservaEmergencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    familia_id = db.Column(db.Integer, db.ForeignKey('familia.id'), nullable=False)

# Decorator para rotas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Inicializar banco e usuários padrão
with app.app_context():
    db.create_all()
    
    # Família padrão removida - use criar_banco_novo.py para popular dados
    pass

# Rotas de Páginas
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'criar_familia':
            # Criar nova família
            import secrets
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
            
            return redirect(url_for('dashboard'))
        
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
            
            return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
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
            
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Usuário ou senha inválidos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    familia = Familia.query.get(session.get('familia_id'))
    return render_template('dashboard.html', meta_reserva=familia.meta_reserva if familia else 40500.00)

@app.route('/receitas')
@login_required
def receitas_page():
    return render_template('receitas.html')

@app.route('/despesas-fixas')
@login_required
def despesas_fixas_page():
    return render_template('despesas_fixas.html')

@app.route('/despesas-variaveis')
@login_required
def despesas_variaveis_page():
    return render_template('despesas_variaveis.html')

@app.route('/reserva')
@login_required
def reserva_page():
    familia = Familia.query.get(session.get('familia_id'))
    return render_template('reserva.html', meta_reserva=familia.meta_reserva if familia else 40500.00)

@app.route('/api/atualizar-meta-reserva', methods=['POST'])
@login_required
def atualizar_meta_reserva():
    familia_id = session.get('familia_id')
    familia = Familia.query.get(familia_id)
    
    if not familia:
        return jsonify({'error': 'Família não encontrada'}), 404
    
    data = request.get_json()
    nova_meta = data.get('meta')
    
    if not nova_meta or nova_meta <= 0:
        return jsonify({'error': 'Meta inválida'}), 400
    
    familia.meta_reserva = nova_meta
    db.session.commit()
    
    return jsonify({'success': True, 'meta': nova_meta})

@app.route('/planos')
def planos_page():
    return render_template('planos.html')

# API Routes
@app.route('/api/dashboard-data')
@login_required
def dashboard_data():
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    familia_id = session.get('familia_id')
    
    receitas = db.session.query(db.func.sum(Receita.valor)).filter(
        Receita.mes == mes,
        Receita.ano == ano,
        Receita.familia_id == familia_id
    ).scalar() or 0
    # Apenas despesas PAGAS são descontadas
    despesas_fixas = db.session.query(db.func.sum(DespesaFixa.valor)).filter(
        DespesaFixa.mes == mes,
        DespesaFixa.ano == ano,
        DespesaFixa.pago == True,  # Apenas pagas
        DespesaFixa.familia_id == familia_id
    ).scalar() or 0
    
    despesas_variaveis = db.session.query(db.func.sum(DespesaVariavel.valor)).filter(
        db.extract('month', DespesaVariavel.data) == mes,
        db.extract('year', DespesaVariavel.data) == ano,
        DespesaVariavel.familia_id == familia_id
    ).scalar() or 0
    
    reserva = db.session.query(db.func.sum(ReservaEmergencia.valor)).filter(
        ReservaEmergencia.familia_id == familia_id
    ).scalar() or 0
    saldo_disponivel = receitas - despesas_fixas - despesas_variaveis
    
    # Gastos por usuário no mês (gastos variáveis + despesas fixas pagas)
    # Gastos variáveis
    gastos_variaveis_por_usuario = db.session.query(
        User.nome,
        db.func.sum(DespesaVariavel.valor).label('total')
    ).join(User, DespesaVariavel.user_id == User.id).filter(
        db.extract('month', DespesaVariavel.data) == mes,
        db.extract('year', DespesaVariavel.data) == ano,
        DespesaVariavel.familia_id == familia_id
    ).group_by(User.nome).all()
    
    # Despesas fixas pagas
    despesas_fixas_por_usuario = db.session.query(
        User.nome,
        db.func.sum(DespesaFixa.valor).label('total')
    ).join(User, DespesaFixa.pago_por_user_id == User.id).filter(
        DespesaFixa.mes == mes,
        DespesaFixa.ano == ano,
        DespesaFixa.pago == True,
        DespesaFixa.familia_id == familia_id
    ).group_by(User.nome).all()
    
    # Combinar os dois
    gastos_dict = {}
    for nome, total in gastos_variaveis_por_usuario:
        gastos_dict[nome] = float(total or 0)
    
    for nome, total in despesas_fixas_por_usuario:
        gastos_dict[nome] = gastos_dict.get(nome, 0) + float(total or 0)
    
    gastos_por_usuario = [{'nome': nome, 'total': total} for nome, total in gastos_dict.items()]
    
    return jsonify({
        'receitas': float(receitas),
        'despesas_fixas': float(despesas_fixas),
        'despesas_variaveis': float(despesas_variaveis),
        'saldo_disponivel': float(saldo_disponivel),
        'reserva_emergencia': float(reserva),
        'mes': mes,
        'ano': ano,
        'gastos_por_usuario': gastos_por_usuario
    })

@app.route('/api/receitas', methods=['GET', 'POST'])
@login_required
def api_receitas():
    familia_id = session.get('familia_id')
    
    if request.method == 'GET':
        mes = request.args.get('mes', datetime.now().month, type=int)
        ano = request.args.get('ano', datetime.now().year, type=int)
        receitas = Receita.query.filter_by(mes=mes, ano=ano, familia_id=familia_id).all()
        
        result = []
        for r in receitas:
            usuario = User.query.get(r.user_id).nome if r.user_id else 'Sistema'
            result.append({
                'id': r.id, 
                'descricao': r.descricao, 
                'valor': r.valor,
                'usuario': usuario,
                'mes': r.mes,
                'ano': r.ano
            })
        
        return jsonify(result)
    
    data = request.get_json()
    receita = Receita(
        descricao=data['descricao'], 
        valor=data['valor'],
        mes=data.get('mes', datetime.now().month),
        ano=data.get('ano', datetime.now().year),
        user_id=session['user_id'],
        familia_id=familia_id
    )
    db.session.add(receita)
    db.session.commit()
    return jsonify({
        'id': receita.id, 
        'descricao': receita.descricao, 
        'valor': receita.valor,
        'mes': receita.mes,
        'ano': receita.ano
    }), 201

@app.route('/api/receitas/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_receita_detail(id):
    receita = Receita.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(receita)
        db.session.commit()
        return '', 204
    
    data = request.get_json()
    receita.descricao = data.get('descricao', receita.descricao)
    receita.valor = data.get('valor', receita.valor)
    db.session.commit()
    return jsonify({
        'id': receita.id,
        'descricao': receita.descricao,
        'valor': receita.valor,
        'mes': receita.mes,
        'ano': receita.ano
    })

@app.route('/api/receitas/duplicar-mes', methods=['POST'])
@login_required
def duplicar_receitas_mes():
    familia_id = session.get('familia_id')
    data = request.get_json()
    mes_origem = data['mes_origem']
    ano_origem = data['ano_origem']
    mes_destino = data['mes_destino']
    ano_destino = data['ano_destino']
    
    # Verificar se já existem receitas no mês destino
    existe = Receita.query.filter_by(mes=mes_destino, ano=ano_destino, familia_id=familia_id).first()
    if existe:
        return jsonify({'error': 'Já existem receitas neste mês'}), 400
    
    # Copiar receitas do mês anterior
    receitas_origem = Receita.query.filter_by(mes=mes_origem, ano=ano_origem, familia_id=familia_id).all()
    
    for r in receitas_origem:
        nova_receita = Receita(
            descricao=r.descricao,
            valor=r.valor,
            mes=mes_destino,
            ano=ano_destino,
            user_id=session['user_id'],
            familia_id=familia_id
        )
        db.session.add(nova_receita)
    
    db.session.commit()
    return jsonify({'success': True, 'total': len(receitas_origem)}), 201

@app.route('/api/despesas-fixas', methods=['GET', 'POST'])
@login_required
def api_despesas_fixas():
    familia_id = session.get('familia_id')
    
    if request.method == 'GET':
        mes = request.args.get('mes', datetime.now().month, type=int)
        ano = request.args.get('ano', datetime.now().year, type=int)
        despesas = DespesaFixa.query.filter_by(mes=mes, ano=ano, familia_id=familia_id).all()
        
        result = []
        for d in despesas:
            pago_por = None
            if d.pago_por_user_id:
                user = User.query.get(d.pago_por_user_id)
                pago_por = user.nome if user else None
            
            result.append({
                'id': d.id, 
                'categoria': d.categoria, 
                'descricao': d.descricao, 
                'valor': d.valor,
                'pago': d.pago,
                'pago_por': pago_por,
                'data_pagamento': d.data_pagamento.strftime('%d/%m/%Y %H:%M') if d.data_pagamento else None,
                'mes': d.mes,
                'ano': d.ano
            })
        
        return jsonify(result)
    
    data = request.get_json()
    despesa = DespesaFixa(
        categoria=data['categoria'],
        descricao=data['descricao'],
        valor=data['valor'],
        pago=data.get('pago', False),
        mes=data.get('mes', datetime.now().month),
        ano=data.get('ano', datetime.now().year),
        user_id=session['user_id'],
        familia_id=familia_id
    )
    db.session.add(despesa)
    db.session.commit()
    return jsonify({
        'id': despesa.id,
        'categoria': despesa.categoria,
        'descricao': despesa.descricao,
        'valor': despesa.valor,
        'pago': despesa.pago,
        'mes': despesa.mes,
        'ano': despesa.ano
    }), 201

@app.route('/api/despesas-fixas/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_despesa_fixa_detail(id):
    despesa = DespesaFixa.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(despesa)
        db.session.commit()
        return '', 204
    
    data = request.get_json()
    
    # Se está marcando como pago, registrar quem pagou e quando
    if 'pago' in data and data['pago'] and not despesa.pago:
        despesa.pago = True
        despesa.pago_por_user_id = session.get('user_id')
        despesa.data_pagamento = datetime.utcnow()
    elif 'pago' in data and not data['pago']:
        # Se está desmarcando, limpar os dados de pagamento
        despesa.pago = False
        despesa.pago_por_user_id = None
        despesa.data_pagamento = None
    
    despesa.valor = data.get('valor', despesa.valor)
    despesa.descricao = data.get('descricao', despesa.descricao)
    despesa.categoria = data.get('categoria', despesa.categoria)
    db.session.commit()
    
    # Buscar nome do usuário que pagou
    pago_por = None
    if despesa.pago_por_user_id:
        user = User.query.get(despesa.pago_por_user_id)
        pago_por = user.nome if user else None
    
    return jsonify({
        'id': despesa.id,
        'categoria': despesa.categoria,
        'descricao': despesa.descricao,
        'valor': despesa.valor,
        'pago': despesa.pago,
        'pago_por': pago_por,
        'data_pagamento': despesa.data_pagamento.strftime('%d/%m/%Y %H:%M') if despesa.data_pagamento else None,
        'mes': despesa.mes,
        'ano': despesa.ano
    })

@app.route('/api/despesas-fixas/duplicar-mes', methods=['POST'])
@login_required
def duplicar_mes():
    familia_id = session.get('familia_id')
    data = request.get_json()
    mes_origem = data['mes_origem']
    ano_origem = data['ano_origem']
    mes_destino = data['mes_destino']
    ano_destino = data['ano_destino']
    
    # Verificar se já existem despesas no mês destino
    existe = DespesaFixa.query.filter_by(mes=mes_destino, ano=ano_destino, familia_id=familia_id).first()
    if existe:
        return jsonify({'error': 'Já existem despesas neste mês'}), 400
    
    # Copiar despesas do mês anterior
    despesas_origem = DespesaFixa.query.filter_by(mes=mes_origem, ano=ano_origem, familia_id=familia_id).all()
    
    for d in despesas_origem:
        nova_despesa = DespesaFixa(
            categoria=d.categoria,
            descricao=d.descricao,
            valor=d.valor,
            pago=False,  # Novo mês começa com tudo não pago
            mes=mes_destino,
            ano=ano_destino,
            user_id=session['user_id'],
            familia_id=familia_id
        )
        db.session.add(nova_despesa)
    
    db.session.commit()
    return jsonify({'success': True, 'total': len(despesas_origem)}), 201

@app.route('/api/despesas-variaveis', methods=['GET', 'POST'])
@login_required
def api_despesas_variaveis():
    familia_id = session.get('familia_id')
    
    if request.method == 'GET':
        mes = request.args.get('mes', datetime.now().month)
        ano = request.args.get('ano', datetime.now().year)
        despesas = DespesaVariavel.query.filter(
            db.extract('month', DespesaVariavel.data) == mes,
            db.extract('year', DespesaVariavel.data) == ano,
            DespesaVariavel.familia_id == familia_id
        ).all()
        return jsonify([{
            'id': d.id,
            'categoria': d.categoria,
            'descricao': d.descricao,
            'valor': d.valor,
            'data': d.data.strftime('%Y-%m-%d'),
            'usuario': User.query.get(d.user_id).nome if d.user_id else 'Sistema'
        } for d in despesas])
    
    data = request.get_json()
    despesa = DespesaVariavel(
        categoria=data['categoria'],
        descricao=data['descricao'],
        valor=data['valor'],
        data=datetime.strptime(data['data'], '%Y-%m-%d'),
        user_id=session['user_id'],
        familia_id=familia_id
    )
    db.session.add(despesa)
    db.session.commit()
    return jsonify({
        'id': despesa.id,
        'categoria': despesa.categoria,
        'descricao': despesa.descricao,
        'valor': despesa.valor,
        'data': despesa.data.strftime('%Y-%m-%d')
    }), 201

@app.route('/api/despesas-variaveis/<int:id>', methods=['DELETE'])
@login_required
def api_despesa_variavel_delete(id):
    despesa = DespesaVariavel.query.get_or_404(id)
    db.session.delete(despesa)
    db.session.commit()
    return '', 204

@app.route('/api/evolucao-mensal', methods=['GET'])
@login_required
def evolucao_mensal():
    familia_id = session.get('familia_id')
    ano = request.args.get('ano', datetime.now().year, type=int)
    
    meses_data = []
    for mes in range(1, 13):
        receitas = db.session.query(db.func.sum(Receita.valor)).filter(
            Receita.mes == mes,
            Receita.ano == ano,
            Receita.familia_id == familia_id
        ).scalar() or 0
        
        despesas_fixas = db.session.query(db.func.sum(DespesaFixa.valor)).filter(
            DespesaFixa.mes == mes,
            DespesaFixa.ano == ano,
            DespesaFixa.familia_id == familia_id
        ).scalar() or 0
        
        despesas_variaveis = db.session.query(db.func.sum(DespesaVariavel.valor)).filter(
            db.extract('month', DespesaVariavel.data) == mes,
            db.extract('year', DespesaVariavel.data) == ano,
            DespesaVariavel.familia_id == familia_id
        ).scalar() or 0
        
        saldo = receitas - despesas_fixas - despesas_variaveis
        
        meses_data.append({
            'mes': mes,
            'receitas': float(receitas),
            'despesas_fixas': float(despesas_fixas),
            'despesas_variaveis': float(despesas_variaveis),
            'saldo': float(saldo)
        })
    
    return jsonify(meses_data)

@app.route('/api/reserva-emergencia', methods=['GET', 'POST'])
@login_required
def api_reserva():
    familia_id = session.get('familia_id')
    
    if request.method == 'GET':
        reservas = ReservaEmergencia.query.filter_by(familia_id=familia_id).order_by(ReservaEmergencia.data.desc()).all()
        total = db.session.query(db.func.sum(ReservaEmergencia.valor)).filter_by(familia_id=familia_id).scalar() or 0
        return jsonify({
            'historico': [{
                'id': r.id,
                'valor': r.valor,
                'data': r.data.strftime('%Y-%m-%d'),
                'observacao': r.observacao,
                'usuario': User.query.get(r.user_id).nome if r.user_id else 'Sistema'
            } for r in reservas],
            'total': float(total)
        })
    
    data = request.get_json()
    reserva = ReservaEmergencia(
        valor=data['valor'],
        data=datetime.strptime(data['data'], '%Y-%m-%d'),
        observacao=data.get('observacao', ''),
        user_id=session['user_id'],
        familia_id=familia_id
    )
    db.session.add(reserva)
    db.session.commit()
    return jsonify({
        'id': reserva.id,
        'valor': reserva.valor,
        'data': reserva.data.strftime('%Y-%m-%d'),
        'observacao': reserva.observacao
    }), 201

@app.route('/api/reserva-emergencia/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_reserva_detail(id):
    reserva = ReservaEmergencia.query.get_or_404(id)
    
    # Verificar se pertence à família do usuário
    if reserva.familia_id != session.get('familia_id'):
        return jsonify({'error': 'Acesso negado'}), 403
    
    if request.method == 'DELETE':
        db.session.delete(reserva)
        db.session.commit()
        return '', 204
    
    # PUT - Atualizar
    data = request.get_json()
    reserva.valor = data.get('valor', reserva.valor)
    reserva.data = datetime.strptime(data['data'], '%Y-%m-%d') if 'data' in data else reserva.data
    reserva.observacao = data.get('observacao', reserva.observacao)
    db.session.commit()
    
    return jsonify({
        'id': reserva.id,
        'valor': reserva.valor,
        'data': reserva.data.strftime('%Y-%m-%d'),
        'observacao': reserva.observacao
    })

# ==================== PAINEL ADMIN ====================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        
        user = User.query.get(session.get('user_id'))
        if not user or not user.is_admin:
            return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
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

@app.route('/admin/familias')
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

@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    usuarios = User.query.order_by(User.id.desc()).all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/api/stats')
@admin_required
def admin_api_stats():
    # Estatísticas em tempo real para gráficos
    
    # Crescimento mensal de famílias (últimos 12 meses)
    from datetime import datetime, timedelta
    hoje = datetime.now()
    crescimento = []
    
    for i in range(11, -1, -1):
        mes_ref = hoje - timedelta(days=30*i)
        count = Familia.query.filter(
            db.func.strftime('%Y-%m', Familia.created_at) == mes_ref.strftime('%Y-%m')
        ).count()
        crescimento.append({
            'mes': mes_ref.strftime('%b/%y'),
            'count': count
        })
    
    return jsonify({
        'crescimento_familias': crescimento,
        'distribuicao_planos': {
            'free': Familia.query.filter_by(plano='free').count(),
            'premium': Familia.query.filter_by(plano='premium').count(),
            'vip': Familia.query.filter_by(plano='vip').count()
        }
    })

@app.route('/admin/tornar-admin/<int:user_id>', methods=['POST'])
@admin_required
def tornar_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    user.is_admin = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{user.nome} agora é admin!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
