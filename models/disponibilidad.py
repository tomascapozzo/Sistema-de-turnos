from sqlalchemy import Column, Integer, String, Time, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
import enum

class DiaSemana(enum.Enum):
    Lunes = 'Lunes'
    Martes = 'Martes'
    Miercoles = 'Miercoles'
    Jueves = 'Jueves'
    Viernes = 'Viernes'
    Sabado = 'Sabado'
    Domingo = 'Domingo'

class Disponibilidad(Base):
    __tablename__ = 'disponibilidades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    profesional_id = Column(Integer, ForeignKey('profesionales.id'))
    dia = Column(Enum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    profesional = relationship('Profesional', back_populates='disponibilidades')