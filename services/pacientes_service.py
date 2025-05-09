from models.paciente import Paciente

def agregarpaciente(db, nombre, apellido, email, telefono):

    existe = db.query(Paciente).filter(Paciente.email == email).first()
    if existe:
        return {'error': 'Paciente ya existente'}


    #for p in pacientes:
    #    if p.email == email:
    #        return {"error": "Ya existe un paciente con ese email."}

    nuevopaciente = Paciente(
        nombre=nombre,
        apellido=apellido,
        email=email,
        telefono=telefono,
    )

    db.add(nuevopaciente)
    db.commit()
    db.refresh(nuevopaciente)
    return {"mensaje": "Paciente creado con éxito", "paciente_id": nuevopaciente.id}

def obtener_nombre_paciente(db, paciente_id):
    #for p in pacientes:
    #    if p.id == paciente_id:
    #        return f"{p.nombre} {p.apellido}"
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if paciente:
        return f"{paciente.nombre} {paciente.apellido}"
    return "Paciente desconocido"