from flask import Flask, render_template, request, redirect, url_for

from models.paciente import Paciente
from models.profesional import Profesional
from services.turno_service import  agregarturno, obtener_turnos
from services.pacientes_service import  obtener_nombre_paciente, agregarpaciente
from services.profesional_service import obtener_nombre_profesional, agregarprofesional
from models import *
from datetime import datetime
from database.db import SessionLocal
from database.db import Base, engine

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/turnos/nuevo', methods=['GET', 'POST'])
def nuevo_turno():
    db = SessionLocal()
    if request.method == 'POST':
        try:
            paciente_id = int(request.form['paciente_id'])
            profesional_id = int(request.form['profesional_id'])
            fecha = request.form['fecha']
            hora = request.form['hora']

            resultado = agregarturno(db, paciente_id, profesional_id, fecha, hora)

            if "error" in resultado:
                return resultado["error"], 400

            return redirect(url_for('listar_turnos'))

        finally:
            db.close()

    return render_template('crear_turno.html')

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
            telefono = request.form['telefone']

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
            telefono = request.form['telefone']
            especialidad = request.form['especialidad']

            resultado = agregarprofesional(db, nombre, apellido, email, telefono, especialidad)

            if 'error' in resultado:
                return resultado["error"], 400
            return redirect(url_for('listar_profesionales'))
        finally:
            db.close()
    return render_template('crear_profesional.html')

if __name__ == '__main__':
    app.run(debug=True)
