from sqlalchemy.orm import Session
from datetime import datetime, date, time
from models.turno import Turno, EstadoTurno

def agregarturno(db:Session, paciente_id: int, profesional_id: int, fecha: str, hora: str):
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    hora = datetime.strptime(hora, '%H:%M').time()

    existe = db.query(Turno).filter(
        Turno.profesional_id == profesional_id,
        Turno.fecha == fecha,
        Turno.hora == hora,
    ).first()

    if existe:
        return {'error': 'El profesional no tiene disponibilidad en ese horario.'}
    #for t in turnos:
     #  if t.profesional_id == profesional_id and t.fecha == fecha and t.hora == hora:
      #    return {'error': 'El profesional no tiene disponibilidad en ese turno.'}

    nuevoturno = Turno(
        paciente_id=paciente_id,
        profesional_id=profesional_id,
        fecha=fecha,
        hora=hora,
        estado=EstadoTurno.PENDIENTE
    )
    db.add(nuevoturno)
    db.commit()
    db.refresh(nuevoturno)
    return {"mensaje": "Turno creado con éxito", "turno_id": nuevoturno.id}

def obtener_turnos(db: Session):
    return db.query(Turno).all()