from app import create_app, db
from app.models.finance import DespesaFixa
from app.models.core import User, Familia
from app.routes.api import verificar_recorrencia
from datetime import datetime

app = create_app()

def verify_recurrence():
    with app.app_context():
        print("🔍 Iniciando verificação de recorrência...")
        
        # 1. Setup: Criar uma despesa recorrente no mês passado
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        
        if mes_atual == 1:
            mes_anterior = 12
            ano_anterior = ano_atual - 1
        else:
            mes_anterior = mes_atual - 1
            ano_anterior = ano_atual
            
        # Pegar um usuário e família existentes (assumindo id 1)
        user = User.query.first()
        if not user:
            print("❌ Nenhum usuário encontrado.")
            return

        print(f"📅 Mês Atual: {mes_atual}/{ano_atual}")
        print(f"📅 Mês Anterior: {mes_anterior}/{ano_anterior}")
        
        # Limpar despesas de teste anteriores
        DespesaFixa.query.filter_by(descricao="Teste Recorrência").delete()
        db.session.commit()
        
        # Criar despesa no mês passado
        despesa_antiga = DespesaFixa(
            categoria="Outros",
            descricao="Teste Recorrência",
            valor=100.00,
            mes=mes_anterior,
            ano=ano_anterior,
            recorrente=True,
            dia_vencimento=15,
            user_id=user.id,
            familia_id=user.familia_id
        )
        db.session.add(despesa_antiga)
        db.session.commit()
        print("✅ Despesa recorrente criada no mês anterior.")
        
        # 2. Executar a verificação
        verificar_recorrencia(user.familia_id, mes_atual, ano_atual)
        
        # 3. Verificar se foi criada no mês atual
        nova_despesa = DespesaFixa.query.filter_by(
            familia_id=user.familia_id,
            mes=mes_atual,
            ano=ano_atual,
            descricao="Teste Recorrência"
        ).first()
        
        if nova_despesa:
            print(f"✅ SUCESSO! Despesa recorrente gerada automaticamente: ID {nova_despesa.id}")
            print(f"   Valor: {nova_despesa.valor}, Vencimento: {nova_despesa.dia_vencimento}")
            
            # Limpeza
            db.session.delete(despesa_antiga)
            db.session.delete(nova_despesa)
            db.session.commit()
            print("🧹 Dados de teste limpos.")
        else:
            print("❌ FALHA! A despesa não foi gerada automaticamente.")

if __name__ == "__main__":
    verify_recurrence()
