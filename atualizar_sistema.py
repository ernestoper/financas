#!/usr/bin/env python3
"""
Script para atualizar o sistema com as novas funcionalidades
- Adiciona relacionamento User -> Familia
- Adiciona campos pago_por_user_id e data_pagamento em DespesaFixa
- Mantém todos os dados existentes
"""

from app import app, db
import sqlite3

def atualizar_sistema():
    with app.app_context():
        print("🔄 Atualizando sistema...")
        
        # Adicionar novas colunas se não existirem
        conn = sqlite3.connect('instance/financas.db')
        cursor = conn.cursor()
        
        try:
            # Verificar se as colunas já existem
            cursor.execute("PRAGMA table_info(despesa_fixa)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'pago_por_user_id' not in columns:
                print("   Adicionando coluna pago_por_user_id...")
                cursor.execute("ALTER TABLE despesa_fixa ADD COLUMN pago_por_user_id INTEGER")
                
            if 'data_pagamento' not in columns:
                print("   Adicionando coluna data_pagamento...")
                cursor.execute("ALTER TABLE despesa_fixa ADD COLUMN data_pagamento DATETIME")
            
            conn.commit()
            print("   ✓ Colunas adicionadas")
        except Exception as e:
            print(f"   ⚠️  Erro ao adicionar colunas: {e}")
        finally:
            conn.close()
        
        # Criar tabelas se não existirem
        db.create_all()
        
        print("✅ Sistema atualizado com sucesso!")
        print("\n📊 Estatísticas:")
        
        from app import User, Familia, DespesaFixa
        
        total_familias = Familia.query.count()
        total_usuarios = User.query.count()
        admins = User.query.filter_by(is_admin=True).count()
        despesas = DespesaFixa.query.count()
        despesas_pagas = DespesaFixa.query.filter_by(pago=True).count()
        
        print(f"   - Famílias: {total_familias}")
        print(f"   - Usuários: {total_usuarios}")
        print(f"   - Admins: {admins}")
        print(f"   - Despesas fixas: {despesas}")
        print(f"   - Despesas pagas: {despesas_pagas}")
        
        if admins == 0:
            print("\n⚠️  Nenhum admin encontrado!")
            print("   Execute: python tornar_admin.py seu_username")
        
        print("\n🎉 Novidades:")
        print("   ✓ Apenas despesas PAGAS são descontadas do saldo")
        print("   ✓ Sistema registra quem pagou cada despesa")
        print("   ✓ Botão 'Pagar' mais visível nas despesas fixas")
        print("   ✓ Badge de status (PAGO/PENDENTE)")
        print("   ✓ Resumo de contas pagas/pendentes")
        
        print("\n🚀 Pronto para usar!")
        print("   - Iniciar: python app.py")
        print("   - Admin: http://localhost:5000/admin")

if __name__ == '__main__':
    atualizar_sistema()
