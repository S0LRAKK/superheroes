from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Personaje(Base):
    __tablename__ = "personajes"  # Nombre de la tabla en la base de datos

    idpersonaje = Column(Integer, primary_key=True, index=True)
    alias = Column(String, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer, index=True)

class Usuario(Base):
    __tablename__ = "usuarios"  # Nombre de la tabla en la base de datos

    idusuario = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    activa = Column(Boolean, default=True)  # Por ejemplo, para usuarios activados o desactivados