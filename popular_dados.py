"""
Script para popular o banco de dados com os dados financeiros reais
"""
from app import app, db, User, Receita, DespesaFixa

def popular_dados():
    with app.app_context():
        # Limpar dados existentes (exceto usuários)
        Receita.query.delete()
        DespesaFixa.query.delete()
        
        # Pegar o primeiro usuário e família
        user = User.query.first()
        familia_id = user.familia_id if user else 1
        
        # Pegar mês e ano atual
        from datetime import datetime
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
                familia_id=familia_id
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
                familia_id=familia_id
            )
            db.session.add(despesa)
        
        db.session.commit()
        
        from datetime import datetime
        mes_nome = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        print("✅ Dados populados com sucesso!")
        print("\n📊 Resumo:")
        print(f"   Receitas: R$ 8.500,00")
        print(f"   Despesas Fixas: R$ 6.737,51 ({mes_nome[datetime.now().month]}/{datetime.now().year})")
        print(f"   Saldo Disponível: R$ 1.762,49")
        print("\n💡 Dica: Use 'Copiar Mês Anterior' para duplicar despesas nos próximos meses!")
        print("\n🎯 Acesse http://localhost:5000 para ver!")

if __name__ == '__main__':
    popular_dados()
