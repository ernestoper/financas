from flask import Blueprint, jsonify, request, session
from datetime import datetime
from app.extensions import db
from app.models import User, Familia, Receita, DespesaFixa, DespesaVariavel, ReservaEmergencia, MetaCategoria
from app.utils import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/atualizar-meta-reserva', methods=['POST'])
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

@bp.route('/dashboard-data')
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
    
    # Gastos por categoria (Fixas + Variáveis)
    gastos_categoria_dict = {}
    
    # Somar Despesas Fixas por Categoria
    despesas_fixas_cats = db.session.query(
        DespesaFixa.categoria,
        db.func.sum(DespesaFixa.valor)
    ).filter(
        DespesaFixa.mes == mes,
        DespesaFixa.ano == ano,
        DespesaFixa.familia_id == familia_id
    ).group_by(DespesaFixa.categoria).all()
    
    for cat, val in despesas_fixas_cats:
        gastos_categoria_dict[cat] = gastos_categoria_dict.get(cat, 0) + float(val or 0)
        
    # Somar Despesas Variáveis por Categoria
    despesas_variaveis_cats = db.session.query(
        DespesaVariavel.categoria,
        db.func.sum(DespesaVariavel.valor)
    ).filter(
        db.extract('month', DespesaVariavel.data) == mes,
        db.extract('year', DespesaVariavel.data) == ano,
        DespesaVariavel.familia_id == familia_id
    ).group_by(DespesaVariavel.categoria).all()
    
    for cat, val in despesas_variaveis_cats:
        gastos_categoria_dict[cat] = gastos_categoria_dict.get(cat, 0) + float(val or 0)
    
    
    gastos_por_categoria = [{'categoria': cat, 'total': val} for cat, val in gastos_categoria_dict.items()]
    # Ordenar por valor decrescente
    gastos_por_categoria.sort(key=lambda x: x['total'], reverse=True)
    
    # Buscar metas de categoria
    metas = MetaCategoria.query.filter_by(familia_id=familia_id).all()
    metas_dict = {m.categoria: m.valor_limite for m in metas}
    
    # Criar comparação de metas vs realizado
    comparacao_metas = []
    categorias_com_gastos = set(gastos_categoria_dict.keys())
    categorias_com_metas = set(metas_dict.keys())
    todas_categorias = categorias_com_gastos.union(categorias_com_metas)
    
    for cat in todas_categorias:
        gasto = gastos_categoria_dict.get(cat, 0)
        meta = metas_dict.get(cat, 0)
        percentual = (gasto / meta * 100) if meta > 0 else 0
        
        comparacao_metas.append({
            'categoria': cat,
            'gasto': gasto,
            'meta': meta,
            'percentual': round(percentual, 1),
            'status': 'danger' if percentual > 100 else ('warning' if percentual > 80 else 'success')
        })
    
    # Ordenar por percentual decrescente
    comparacao_metas.sort(key=lambda x: x['percentual'], reverse=True)

    return jsonify({
        'receitas': float(receitas),
        'despesas_fixas': float(despesas_fixas),
        'despesas_variaveis': float(despesas_variaveis),
        'saldo_disponivel': float(saldo_disponivel),
        'reserva_emergencia': float(reserva),
        'mes': mes,
        'ano': ano,
        'gastos_por_usuario': gastos_por_usuario,
        'gastos_por_categoria': gastos_por_categoria,
        'comparacao_metas': comparacao_metas
    })

@bp.route('/receitas', methods=['GET', 'POST'])
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

@bp.route('/receitas/<int:id>', methods=['PUT', 'DELETE'])
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

@bp.route('/receitas/duplicar-mes', methods=['POST'])
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

@bp.route('/despesas-fixas', methods=['GET', 'POST'])
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

@bp.route('/despesas-fixas/<int:id>', methods=['PUT', 'DELETE'])
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

@bp.route('/despesas-fixas/duplicar-mes', methods=['POST'])
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

@bp.route('/despesas-variaveis', methods=['GET', 'POST'])
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

@bp.route('/despesas-variaveis/<int:id>', methods=['DELETE'])
@login_required
def api_despesa_variavel_delete(id):
    despesa = DespesaVariavel.query.get_or_404(id)
    db.session.delete(despesa)
    db.session.commit()
    return '', 204

@bp.route('/evolucao-mensal', methods=['GET'])
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

@bp.route('/reserva-emergencia', methods=['GET', 'POST'])
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

@bp.route('/reserva-emergencia/<int:id>', methods=['PUT', 'DELETE'])
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

@bp.route('/metas-categoria', methods=['GET', 'POST'])
@login_required
def api_metas_categoria():
    familia_id = session.get('familia_id')
    
    if request.method == 'GET':
        metas = MetaCategoria.query.filter_by(familia_id=familia_id).all()
        return jsonify([{
            'id': m.id,
            'categoria': m.categoria,
            'valor_limite': m.valor_limite
        } for m in metas])
    
    data = request.get_json()
    
    # Verificar se já existe meta para essa categoria
    existe = MetaCategoria.query.filter_by(
        familia_id=familia_id, 
        categoria=data['categoria']
    ).first()
    
    if existe:
        return jsonify({'error': 'Já existe uma meta para esta categoria'}), 400
        
    meta = MetaCategoria(
        categoria=data['categoria'],
        valor_limite=data['valor_limite'],
        familia_id=familia_id
    )
    db.session.add(meta)
    db.session.commit()
    
    return jsonify({
        'id': meta.id,
        'categoria': meta.categoria,
        'valor_limite': meta.valor_limite
    }), 201

@bp.route('/metas-categoria/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_meta_categoria_detail(id):
    meta = MetaCategoria.query.get_or_404(id)
    
    if meta.familia_id != session.get('familia_id'):
        return jsonify({'error': 'Acesso negado'}), 403
        
    if request.method == 'DELETE':
        db.session.delete(meta)
        db.session.commit()
        return '', 204
        
    data = request.get_json()
    meta.valor_limite = data.get('valor_limite', meta.valor_limite)
    db.session.commit()
    
    return jsonify({
        'id': meta.id,
        'categoria': meta.categoria,
        'valor_limite': meta.valor_limite
    })

@bp.route('/exportar', methods=['GET'])
@login_required
def exportar_dados():
    import pandas as pd
    import io
    from flask import send_file
    
    familia_id = session.get('familia_id')
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)
    
    # Filtros básicos
    filters = {'familia_id': familia_id}
    if mes:
        filters['mes'] = mes
    if ano:
        filters['ano'] = ano
        
    # Receitas
    receitas_query = Receita.query.filter_by(familia_id=familia_id)
    if mes: receitas_query = receitas_query.filter_by(mes=mes)
    if ano: receitas_query = receitas_query.filter_by(ano=ano)
    
    receitas_data = [{
        'Descrição': r.descricao,
        'Valor': r.valor,
        'Mês': r.mes,
        'Ano': r.ano,
        'Usuário': User.query.get(r.user_id).nome if r.user_id else 'Sistema'
    } for r in receitas_query.all()]
    
    # Despesas Fixas
    fixas_query = DespesaFixa.query.filter_by(familia_id=familia_id)
    if mes: fixas_query = fixas_query.filter_by(mes=mes)
    if ano: fixas_query = fixas_query.filter_by(ano=ano)
    
    fixas_data = [{
        'Categoria': d.categoria,
        'Descrição': d.descricao,
        'Valor': d.valor,
        'Pago': 'Sim' if d.pago else 'Não',
        'Mês': d.mes,
        'Ano': d.ano
    } for d in fixas_query.all()]
    
    # Despesas Variáveis
    var_query = DespesaVariavel.query.filter_by(familia_id=familia_id)
    if mes: var_query = var_query.filter(db.extract('month', DespesaVariavel.data) == mes)
    if ano: var_query = var_query.filter(db.extract('year', DespesaVariavel.data) == ano)
    
    var_data = [{
        'Categoria': d.categoria,
        'Descrição': d.descricao,
        'Valor': d.valor,
        'Data': d.data.strftime('%d/%m/%Y'),
        'Usuário': User.query.get(d.user_id).nome if d.user_id else 'Sistema'
    } for d in var_query.all()]
    
    # Criar Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(receitas_data).to_excel(writer, sheet_name='Receitas', index=False)
        pd.DataFrame(fixas_data).to_excel(writer, sheet_name='Despesas Fixas', index=False)
        pd.DataFrame(var_data).to_excel(writer, sheet_name='Despesas Variáveis', index=False)
        
    output.seek(0)
    filename = f'relatorio_financeiro_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )
