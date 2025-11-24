from app import create_app, db
from app.models.finance import ReservaGoal, ReservaEmergencia
from app.models import Familia
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Iniciando migração...")
    
    # 1. Criar tabela reserva_goal
    try:
        ReservaGoal.__table__.create(db.engine)
        print("Tabela 'reserva_goal' criada.")
    except Exception as e:
        print(f"Tabela 'reserva_goal' já existe ou erro: {e}")

    # 2. Adicionar coluna goal_id em reserva_emergencia
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE reserva_emergencia ADD COLUMN goal_id INTEGER REFERENCES reserva_goal(id)"))
            print("Coluna 'goal_id' adicionada em 'reserva_emergencia'.")
    except Exception as e:
        print(f"Coluna 'goal_id' já existe ou erro: {e}")

    # 3. Migrar dados existentes
    familias = Familia.query.all()
    for familia in familias:
        # Verificar se já existe um goal padrão
        default_goal = ReservaGoal.query.filter_by(familia_id=familia.id, nome="Reserva de Emergência").first()
        
        if not default_goal:
            # Usar a meta antiga da família como meta do goal, ou um valor padrão
            meta_valor = getattr(familia, 'meta_reserva', 40500.0)
            
            default_goal = ReservaGoal(
                nome="Reserva de Emergência",
                valor_meta=meta_valor,
                familia_id=familia.id,
                cor="#4CAF50",
                icone="fas fa-shield-alt"
            )
            db.session.add(default_goal)
            db.session.commit()
            print(f"Goal padrão criado para família {familia.id}")
        
        # Atualizar reservas antigas para apontar para este goal
        reservas_sem_goal = ReservaEmergencia.query.filter_by(familia_id=familia.id, goal_id=None).all()
        for reserva in reservas_sem_goal:
            reserva.goal_id = default_goal.id
        
        if reservas_sem_goal:
            db.session.commit()
            print(f"{len(reservas_sem_goal)} reservas atualizadas para a família {familia.id}")

    print("Migração concluída!")
