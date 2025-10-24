import uuid
from database.config import Base
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Persona(Base):
    __tablename__ = "personas"

    id_persona = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Persona(id_persona={self.id_persona}, nombre='{self.nombre}')>"
