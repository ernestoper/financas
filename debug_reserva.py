from app import create_app, db
from app.models import ReservaEmergencia, Familia

app = create_app()

with app.app_context():
    print("--- Verificando Reserva de Emergência ---")
    
    # Verificar famílias
    familias = Familia.query.all()
    print(f"\nFamílias cadastradas: {len(familias)}")
    for f in familias:
        print(f"  - ID: {f.id}, Nome: {f.nome}, Meta: R$ {f.meta_reserva}")
    
    # Verificar reservas
    reservas = ReservaEmergencia.query.all()
    print(f"\nReservas cadastradas: {len(reservas)}")
    for r in reservas:
        print(f"  - ID: {r.id}, Valor: R$ {r.valor}, Data: {r.data}, Família: {r.familia_id}")
    
    # Calcular total por família
    print("\n--- Total por Família ---")
    for f in familias:
        total = db.session.query(db.func.sum(ReservaEmergencia.valor)).filter_by(familia_id=f.id).scalar() or 0
        percentual = (total / f.meta_reserva * 100) if f.meta_reserva > 0 else 0
        print(f"Família {f.nome}: R$ {total:.2f} / R$ {f.meta_reserva:.2f} = {percentual:.1f}%")
