from app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate():
    with app.app_context():
        print("Iniciando migração de Recorrência e Perfil...")
        
        # 1. Adicionar colunas em DespesaFixa
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE despesa_fixa ADD COLUMN recorrente BOOLEAN DEFAULT 0"))
                conn.execute(text("ALTER TABLE despesa_fixa ADD COLUMN dia_vencimento INTEGER"))
                conn.commit()
            print("✅ Colunas 'recorrente' e 'dia_vencimento' adicionadas em 'despesa_fixa'.")
        except Exception as e:
            print(f"⚠️  Erro ao alterar 'despesa_fixa' (pode já existir): {e}")

        # 2. Adicionar coluna em User
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE user ADD COLUMN avatar VARCHAR(50) DEFAULT 'default.png'"))
                conn.commit()
            print("✅ Coluna 'avatar' adicionada em 'user'.")
        except Exception as e:
            print(f"⚠️  Erro ao alterar 'user' (pode já existir): {e}")
            
        print("Migração concluída!")

if __name__ == "__main__":
    migrate()
