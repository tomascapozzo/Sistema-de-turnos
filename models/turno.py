from enum import Enum
from sqlalchemy import Column, Integer, Date, Time, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from database.db import Base
from models.paciente import Paciente
from models.profesional import Profesional

class EstadoTurno(Enum):
    PENDIENTE = 'PENDIENTE'
    ASISTIDO = 'ASISTIDO'
    CANCELADO = 'CANCELADO'

class Turno(Base):
    __tablename__ = 'turnos'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    profesional_id = Column(Integer, ForeignKey('profesionales.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(100), nullable=False)

    paciente = relationship('Paciente', backref='paciente')
    profesional = relationship('Profesional', backref='profesional')