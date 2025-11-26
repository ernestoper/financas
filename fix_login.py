from app import create_app
from app.extensions import db
from app.models.core import User, Familia
from config import get_config

app = create_app(get_config())

with app.app_context():
    # Verificar Família
    familia = Familia.query.first()
    if not familia:
        print("Criando família padrão...")
        familia = Familia(
            nome="Família Padrão",
            codigo_convite="FAMILIA123"
        )
        db.session.add(familia)
        db.session.commit()
    
    # Verificar Usuário
    user = User.query.filter_by(username='ernesto').first()
    if user:
        print(f"Usuário 'ernesto' encontrado. Atualizando senha...")
        user.set_password('senha123')
        user.is_admin = True # Garantir admin para debug
    else:
        print("Usuário 'ernesto' não encontrado. Criando...")
        user = User(
            username='ernesto',
            nome='Ernesto',
            familia_id=familia.id,
            is_admin=True
        )
        user.set_password('senha123')
        db.session.add(user)
    
    try:
        db.session.commit()
        print("Sucesso! Usuário 'ernesto' configurado com senha 'senha123'.")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        db.session.rollback()
