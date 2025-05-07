from sqlalchemy import Column, Integer, String
from database.db import Base
from enum import Enum

class Especialidades(Enum):
    TERAPISTA = 'Terapista Ocupacional'
    PSICOLOGO = 'Psicologia'
    PSICOPEDAGOGO = 'Psicopedagogia'
    PSIQUIATRA = 'Psiquiatria'
    FONOAUDIOLOGO = 'Fonoaudiologia'

class Profesional(Base):
    __tablename__ = 'profesionales'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    especialidades = Column(String(100), nullable=False)