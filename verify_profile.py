from app import create_app, db
from app.models.core import User
from flask import session

app = create_app()

def verify_profile():
    with app.app_context():
        print("🔍 Iniciando verificação de perfil...")
        
        # Setup: Pegar usuário
        user = User.query.first()
        if not user:
            print("❌ Nenhum usuário encontrado.")
            return
            
        original_name = user.nome
        original_avatar = user.avatar
        original_password_hash = user.password_hash
        
        print(f"👤 Usuário: {user.nome}, Avatar: {user.avatar}")
        
        # 1. Testar atualização de Nome
        new_name = "Nome Teste Verificação"
        user.nome = new_name
        db.session.commit()
        
        updated_user = User.query.get(user.id)
        if updated_user.nome == new_name:
            print("✅ Nome atualizado com sucesso.")
        else:
            print("❌ Falha ao atualizar nome.")
            
        # 2. Testar atualização de Avatar
        new_avatar = "👽"
        user.avatar = new_avatar
        db.session.commit()
        
        updated_user = User.query.get(user.id)
        if updated_user.avatar == new_avatar:
            print("✅ Avatar atualizado com sucesso.")
        else:
            print("❌ Falha ao atualizar avatar.")
            
        # 3. Testar atualização de Senha
        new_password = "nova_senha_teste"
        user.set_password(new_password)
        db.session.commit()
        
        updated_user = User.query.get(user.id)
        if updated_user.check_password(new_password):
            print("✅ Senha atualizada e verificada com sucesso.")
        else:
            print("❌ Falha ao atualizar senha.")
            
        # Reverter alterações
        user.nome = original_name
        user.avatar = original_avatar
        user.password_hash = original_password_hash
        db.session.commit()
        print("🔄 Alterações revertidas.")

if __name__ == "__main__":
    verify_profile()
