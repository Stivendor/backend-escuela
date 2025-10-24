import uuid
from database.config import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    rol = Column(String(20), nullable=False)
    profesor_id = Column(
        UUID(as_uuid=True), ForeignKey("profesores.id_profesor"), nullable=True
    )
    estudiante_id = Column(
        UUID(as_uuid=True), ForeignKey("estudiantes.id_estudiante"), nullable=True
    )
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    profesor = relationship("Profesor", backref="usuarios")
    estudiante = relationship("Estudiante", backref="usuarios")

    def __repr__(self):
        return f"<Usuario(username='{self.username}', rol='{self.rol}')>"
