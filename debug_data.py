from app import create_app, db
from app.models import DespesaFixa, DespesaVariavel
from sqlalchemy import func

app = create_app()

with app.app_context():
    mes = 11
    ano = 2025
    
    print(f"--- Debugging Data for {mes}/{ano} ---")
    
    # Check DespesaFixa
    fixas = DespesaFixa.query.filter_by(mes=mes, ano=ano).all()
    print(f"Total Despesas Fixas: {len(fixas)}")
    for f in fixas:
        print(f"  - ID: {f.id}, Cat: {f.categoria}, Valor: {f.valor}, Pago: {f.pago}, Familia: {f.familia_id}")

    # Check DespesaVariavel
    variaveis = DespesaVariavel.query.filter(
        db.extract('month', DespesaVariavel.data) == mes,
        db.extract('year', DespesaVariavel.data) == ano
    ).all()
    print(f"Total Despesas Variáveis: {len(variaveis)}")
    for v in variaveis:
        print(f"  - ID: {v.id}, Cat: {v.categoria}, Valor: {v.valor}, Data: {v.data}, Familia: {v.familia_id}")
