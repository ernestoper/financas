"""
Script para criar banco de dados do zero com a estrutura correta
"""
import os
from datetime import datetime

# Criar pasta instance se não existir
if not os.path.exists('instance'):
    os.makedirs('instance')

# Remover banco antigo se existir
if os.path.exists('instance/financas.db'):
    os.remove('instance/financas.db')
    print("🗑️  Banco antigo removido")

# Agora importar e criar
from app import create_app, db
from app.models import User, Familia, Receita, DespesaFixa, DespesaVariavel, ReservaEmergencia, MetaCategoria

app = create_app()

with app.app_context():
    print("Apagando banco de dados antigo...")
    db.drop_all()
    
    print("Criando novas tabelas...")
    db.create_all()
    
    print("Banco de dados recriado com sucesso!")
    
    # Criar família primeiro
    familia = Familia(
        nome='Família Amaral Juscamayta',
        codigo_convite=secrets.token_urlsafe(8),
        plano='free',
        meta_reserva=40500.00
    )
    db.session.add(familia)
    db.session.commit()
    print(f"✅ Família criada! Código: {familia.codigo_convite}")
    
    # Criar usuários
    if not User.query.filter_by(username='ernesto').first():
        user1 = User(username='ernesto', nome='Ernesto', familia_id=familia.id, is_admin=True)
        user1.set_password('senha123')
        db.session.add(user1)
        
        user2 = User(username='antonietta', nome='Antonietta', familia_id=familia.id, is_admin=False)
        user2.set_password('senha123')
        db.session.add(user2)
        
        db.session.commit()
        print("✅ Usuários criados: ernesto (admin) e antonietta")
    
    # Popular dados
    user = User.query.first()
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    # RECEITAS
    receitas = [
        {'descricao': 'Entrada 1', 'valor': 4600.00},
        {'descricao': 'Entrada 2', 'valor': 3900.00}
    ]
    
    for r in receitas:
        receita = Receita(
            descricao=r['descricao'],
            valor=r['valor'],
            mes=mes_atual,
            ano=ano_atual,
            user_id=user.id,
            familia_id=familia.id
        )
        db.session.add(receita)
    
    # DESPESAS FIXAS
    despesas = [
        # Moradia
        {'categoria': 'Moradia', 'descricao': 'Aluguel', 'valor': 900.00},
        {'categoria': 'Moradia', 'descricao': 'Luz', 'valor': 500.00},
        {'categoria': 'Moradia', 'descricao': 'Água (Compesa)', 'valor': 90.00},
        {'categoria': 'Moradia', 'descricao': 'Internet', 'valor': 110.00},
        {'categoria': 'Moradia', 'descricao': 'Faxina', 'valor': 500.00},
        
        # Transporte
        {'categoria': 'Transporte', 'descricao': 'Passagem', 'valor': 150.00},
        {'categoria': 'Transporte', 'descricao': 'Carona', 'valor': 150.00},
        
        # Saúde
        {'categoria': 'Saúde', 'descricao': 'Plano de saúde (criança)', 'valor': 331.00},
        
        # Educação
        {'categoria': 'Educação', 'descricao': 'Hotelzinho/Escola', 'valor': 600.00},
        
        # Pessoal
        {'categoria': 'Outros', 'descricao': 'Corte de cabelo (Ernesto)', 'valor': 50.00},
        {'categoria': 'Outros', 'descricao': 'MEI', 'valor': 160.00},
        
        # Alimentação
        {'categoria': 'Alimentação', 'descricao': 'Compras mensais', 'valor': 1200.00},
        {'categoria': 'Alimentação', 'descricao': 'Proteínas', 'valor': 200.00},
        
        # Pet
        {'categoria': 'Pet', 'descricao': 'Ração cachorro', 'valor': 100.00},
        {'categoria': 'Pet', 'descricao': 'Sardinhas', 'valor': 200.00},
        {'categoria': 'Pet', 'descricao': 'Vacinas (reserva mensal)', 'valor': 25.00},
        
        # Criança
        {'categoria': 'Criança', 'descricao': 'Fraldas', 'valor': 150.00},
        {'categoria': 'Criança', 'descricao': 'Medicamentos', 'valor': 100.00},
        {'categoria': 'Criança', 'descricao': 'Roupas (média mensal)', 'valor': 150.00},
        {'categoria': 'Criança', 'descricao': 'Passeios e lazer', 'valor': 200.00},
        
        # Vestuário
        {'categoria': 'Vestuário', 'descricao': 'Roupas adultos (média)', 'valor': 100.00},
        
        # Streaming
        {'categoria': 'Streaming', 'descricao': 'Netflix', 'valor': 20.90},
        {'categoria': 'Streaming', 'descricao': 'Amazon Prime', 'valor': 13.90},
        {'categoria': 'Streaming', 'descricao': 'Apple TV', 'valor': 28.00},
        {'categoria': 'Streaming', 'descricao': 'Disney+', 'valor': 9.90},
        
        # Dívidas
        {'categoria': 'Outros', 'descricao': 'Negociação de dívidas', 'valor': 200.00},
        {'categoria': 'Outros', 'descricao': 'Cartão IA (uso mensal)', 'valor': 120.00},
        
        # Parcelamentos (temporários - 3 meses restantes)
        {'categoria': 'Outros', 'descricao': 'Peça computador 1 (3x)', 'valor': 167.65},
        {'categoria': 'Outros', 'descricao': 'Peça computador 2 (3x)', 'valor': 83.82},
        {'categoria': 'Outros', 'descricao': 'Peça computador 3 (3x)', 'valor': 127.34},
    ]
    
    for d in despesas:
        despesa = DespesaFixa(
            categoria=d['categoria'],
            descricao=d['descricao'],
            valor=d['valor'],
            pago=False,
            mes=mes_atual,
            ano=ano_atual,
            user_id=user.id,
            familia_id=familia.id
        )
        db.session.add(despesa)
    
    db.session.commit()
    
    mes_nome = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    print("\n✅ Dados populados com sucesso!")
    print("\n📊 Resumo:")
    print(f"   Receitas: R$ 8.500,00")
    print(f"   Despesas Fixas: R$ 6.737,51 ({mes_nome[mes_atual]}/{ano_atual})")
    print(f"   Saldo Disponível: R$ 1.762,49")
    print("\n💡 Dica: Use 'Copiar Mês Anterior' para duplicar despesas nos próximos meses!")
    print("\n🎯 Acesse http://localhost:5000 para ver!")
