from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    direcciones = relationship("Direccion", back_populates="usuario", cascade="all, delete-orphan")

class Direccion(Base):
    __tablename__ = "direcciones"

    id_direccion = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    calle_numero = Column(String(255), nullable=False)
    distrito = Column(String(100), nullable=False)
    referencia = Column(String(255), nullable=True)

    usuario = relationship("Usuario", back_populates="direcciones")