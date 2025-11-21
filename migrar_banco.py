"""
Script para migrar o banco de dados existente para o novo formato com mês/ano
"""
import sqlite3
from datetime import datetime

def migrar_banco():
    conn = sqlite3.connect('financas.db')
    cursor = conn.cursor()
    
    try:
        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(despesa_fixa)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'mes' not in colunas:
            print("📊 Adicionando coluna 'mes' na tabela despesa_fixa...")
            mes_atual = datetime.now().month
            cursor.execute(f"ALTER TABLE despesa_fixa ADD COLUMN mes INTEGER DEFAULT {mes_atual}")
            cursor.execute(f"UPDATE despesa_fixa SET mes = {mes_atual} WHERE mes IS NULL")
            print("✅ Coluna 'mes' adicionada!")
        
        if 'ano' not in colunas:
            print("📊 Adicionando coluna 'ano' na tabela despesa_fixa...")
            ano_atual = datetime.now().year
            cursor.execute(f"ALTER TABLE despesa_fixa ADD COLUMN ano INTEGER DEFAULT {ano_atual}")
            cursor.execute(f"UPDATE despesa_fixa SET ano = {ano_atual} WHERE ano IS NULL")
            print("✅ Coluna 'ano' adicionada!")
        
        conn.commit()
        print("\n✅ Migração concluída com sucesso!")
        print(f"📅 Todas as despesas foram atribuídas a {datetime.now().strftime('%B/%Y')}")
        print("\n💡 Agora você pode:")
        print("   1. Usar o sistema normalmente")
        print("   2. Copiar despesas para o próximo mês")
        print("   3. Editar valores mês a mês")
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("🔄 Iniciando migração do banco de dados...\n")
    migrar_banco()
