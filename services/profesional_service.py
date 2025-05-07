from models.profesional import Profesional, Especialidades
from sqlalchemy.orm import Session



def agregarprofesional(db, nombre, apellido, email, telefono, especialidad):
    #for p in profesionales:
    #    if p.email == email:
    #        return {'error': 'Profesional existente'}
    existe = db.query(Profesional).filter(Profesional.nombre == nombre).first()
    if existe:
        return f"Profesional ya existenste"


    nuevoprofesional = Profesional(
        nombre = nombre,
        apellido = apellido,
        email = email,
        telefono = telefono,
        especialidades = especialidad
    )
    db.add(nuevoprofesional)
    db.commit()
    db.refresh(nuevoprofesional)
    return {'mensaje': 'Profesional creado correctamente'}

def obtener_nombre_profesional(db, profesional_id):
    profesional = db.query(Profesional).get(profesional_id)
    if profesional:
        return f"{profesional.nombre} {profesional.apellido}"
    return 'Profesional inexistente'

def obtener_profesionales(db: Session):
    profesionales = db.query(Profesional).all()
