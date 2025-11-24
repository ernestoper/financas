from app import create_app, db
from app.models.core import User, Familia
from flask import session

app = create_app()

def verify_family_update():
    with app.app_context():
        print("🔍 Iniciando verificação de atualização de família...")
        
        # Setup: Pegar usuário e família
        user = User.query.first()
        if not user:
            print("❌ Nenhum usuário encontrado.")
            return
            
        familia = Familia.query.get(user.familia_id)
        original_name = familia.nome
        
        print(f"🏠 Família: {familia.nome}")
        
        # 1. Testar atualização de Nome da Família
        new_name = "Família Teste Verificação"
        familia.nome = new_name
        db.session.commit()
        
        updated_familia = Familia.query.get(familia.id)
        if updated_familia.nome == new_name:
            print("✅ Nome da família atualizado com sucesso.")
        else:
            print("❌ Falha ao atualizar nome da família.")
            
        # Reverter alterações
        familia.nome = original_name
        db.session.commit()
        print("🔄 Alterações revertidas.")

if __name__ == "__main__":
    verify_family_update()
