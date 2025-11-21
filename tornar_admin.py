#!/usr/bin/env python3
"""
Script para tornar um usuário administrador
"""

from app import app, db, User

def tornar_admin(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"❌ Usuário '{username}' não encontrado!")
            print("\nUsuários disponíveis:")
            usuarios = User.query.all()
            for u in usuarios:
                admin_badge = " [ADMIN]" if u.is_admin else ""
                print(f"  - {u.username} ({u.nome}){admin_badge}")
            return
        
        if user.is_admin:
            print(f"✓ {user.nome} já é administrador!")
            return
        
        user.is_admin = True
        db.session.commit()
        
        print(f"✅ {user.nome} agora é ADMINISTRADOR!")
        print(f"\nAcesse o painel admin em: http://localhost:5000/admin")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python tornar_admin.py <username>")
        print("\nExemplo: python tornar_admin.py joao")
        
        with app.app_context():
            usuarios = User.query.all()
            if usuarios:
                print("\nUsuários disponíveis:")
                for u in usuarios:
                    admin_badge = " [ADMIN]" if u.is_admin else ""
                    print(f"  - {u.username} ({u.nome}){admin_badge}")
        sys.exit(1)
    
    username = sys.argv[1]
    tornar_admin(username)
