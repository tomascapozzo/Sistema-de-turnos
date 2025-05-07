from services.turno_service import crearturno, mostrarturnos

from models.paciente import Paciente
from models.profesional import Profesional
from models.turno import Turno

while True:
    print("\n1. Crear Turnos\n2. Ver Turnos\n3. Salir")
    opcion = input('Elegi una opcion: ')
    if opcion == '1':
        paciente_id = input("Paciente ID: ")
        profesional_id = input("Profesional ID: ")
        fecha = input("Fecha: ")
        hora = input("Hora: ")
        resultado = crearturno(paciente_id, profesional_id, fecha, hora)
        print(resultado)
    elif opcion == '2':
        mostrarturnos()
    elif opcion == '3':
        break
    else: print("Opcion invalida.")
