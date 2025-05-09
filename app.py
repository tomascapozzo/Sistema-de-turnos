from flask import Flask, render_template, request, redirect, url_for

from datetime import datetime
from models.paciente import Paciente
from models.profesional import Profesional, Especialidades
from models.turno import Turno
from models.disponibilidad import Disponibilidad, DiaSemana
from services.turno_service import  agregarturno, obtener_turnos
from services.pacientes_service import  obtener_nombre_paciente, agregarpaciente
from services.profesional_service import obtener_nombre_profesional, agregarprofesional
from database.db import SessionLocal
from database.db import Base, engine

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
@app.route('/inicio')
def index():
    return render_template('index.html')

@app.route('/turnos/nuevo', methods=['GET', 'POST'])
def nuevo_turno():
    db = SessionLocal()
    try:
        if request.method == 'POST':
            paciente_id = int(request.form['paciente_id'])
            profesional_id = int(request.form['profesional_id'])
            fecha = request.form['fecha']
            hora = request.form['hora']
            fecha_hora_str = f"{fecha} {hora}"
            fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")

            if fecha_hora < datetime.now():
                return "No se puede asignar un turno en el pasado.", 400

            profesional = db.query(Profesional).get(profesional_id)
            hora_turno = fecha_hora.time()

            if not (profesional.hora_inicio <= hora_turno <= profesional.hora_fin):
                return f"El profesional solo atiende entre {profesional.hora_inicio.strftime('%H:%M')} y {profesional.hora_fin.strftime('%H:%M')}.", 400

            resultado = agregarturno(db, paciente_id, profesional_id, fecha, hora)

            if "error" in resultado:
                return resultado["error"], 400

            return redirect(url_for('listar_turnos'))
        pacientes = db.query(Paciente).all()
        profesionales = db.query(Profesional).all()
        return render_template('crear_turno.html', pacientes=pacientes, profesionales=profesionales)


    finally:
            db.close()



@app.route('/turnos')
def listar_turnos():

    db = SessionLocal()
    lista = obtener_turnos(db)
    db.close()

    return render_template(
        'listar_turnos.html',
        turnos=lista,
        obtener_nombre_paciente=lambda id: obtener_nombre_paciente(db, id),
        obtener_nombre_profesional=lambda id: obtener_nombre_profesional(db, id)
    )

@app.route('/pacientes')
def listar_pacientes():
    db = SessionLocal()
    pacientes = db.query(Paciente).all()
    db.close()
    return render_template('listar_pacientes.html', pacientes=pacientes)

@app.route('/pacientes/nuevo', methods=['GET', 'POST'])
def crear_paciente():
    db = SessionLocal()
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']

            resultado = agregarpaciente(db, nombre, apellido, email, telefono)

            if "error" in resultado:
                return resultado["error"], 400
            return redirect(url_for('listar_pacientes'))
        finally:
            db.close()
    return render_template('crear_paciente.html')

@app.route('/profesionales')
def listar_profesionales():
    db = SessionLocal()
    profesionales = db.query(Profesional).all()
    db.close()
    return render_template('listar_profesionales.html', profesionales=profesionales)
@app.route('/profesionales/nuevo', methods=['GET', 'POST'])
def crear_profesional():
    db = SessionLocal()
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']
            especialidad = request.form['especialidad']
            especial = Especialidades[especialidad].value
            hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
            hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()

            resultado = agregarprofesional(db, nombre, apellido, email, telefono, especial, hora_inicio, hora_fin)



            if 'error' in resultado:
                return resultado["error"], 400
            return redirect(url_for('listar_profesionales'))


        finally:
            db.close()

    return render_template('crear_profesional.html', especialidades = Especialidades)

@app.route('/profesionales/<int:id_profesional>/editar', methods=['GET', 'POST'])
def editar_profesional(id_profesional):
    db = SessionLocal()
    try:
        profesional = db.query(Profesional).filter_by(id=id_profesional).first()
        if not profesional:
            return "Profesional no encontrado", 404

        if request.method == 'POST':
            profesional.nombre = request.form['nombre']
            profesional.apellido = request.form['apellido']
            profesional.email = request.form['email']
            profesional.telefono = request.form['telefono']
            profesional.especialidades = request.form['especialidad']

            dias = request.form.getlist('dia[]')
            horas_inicio = request.form.getlist('hora_inicio[]')
            horas_fin = request.form.getlist('hora_fin[]')

            db.query(Disponibilidad).filter_by(profesional_id=id_profesional).delete()

            for i in range(len(dias)):
                dia = dias[i]
                hora_inicio = datetime.strptime(horas_inicio[i], '%H:%M').time()
                hora_fin = datetime.strptime(horas_fin[i], '%H:%M').time()

                nueva_dispo = Disponibilidad(
                    profesional_id=id_profesional,
                    dia=dia,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                db.add(nueva_dispo)

            db.commit()
            return redirect(url_for('listar_profesionales'))

        return render_template('editar_profesional.html', profesional=profesional)

    finally:
        db.close()
@app.route('/profesionales/<int:profesional_id>')
def ver_profesional(profesional_id):
    db = SessionLocal()
    try:
        profesional = db.query(Profesional).get(profesional_id)
        if not profesional:
            return 'Profesional no encontrado', 404

        turnos = db.query(Turno).filter(Turno.profesional_id == profesional.id).all()

        eventos = [
            {
                'title': f'{t.paciente.nombre} {t.paciente.apellido}',
                'start': f'{t.fecha} {t.hora}',
            }
            for t in turnos
        ]
        return render_template('ficha_profesional.html', profesional=profesional, turnos=turnos, eventos=eventos)
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
