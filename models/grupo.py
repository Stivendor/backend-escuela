import uuid

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

grupo_estudiante = Table(
    "grupo_estudiante",
    Base.metadata,
    Column(
        "grupo_id", UUID(as_uuid=True), ForeignKey("grupos.id_grupo"), primary_key=True
    ),
    Column(
        "estudiante_id",
        UUID(as_uuid=True),
        ForeignKey("estudiantes.id_estudiante"),
        primary_key=True,
    ),
)


class Grupo(Base):
    __tablename__ = "grupos"

    id_grupo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    materia_id = Column(
        UUID(as_uuid=True), ForeignKey("materias.id_materia"), nullable=False
    )
    profesor_id = Column(
        UUID(as_uuid=True), ForeignKey("profesores.id_profesor"), nullable=False
    )

    materia = relationship("Materia", backref="grupos")
    profesor = relationship("Profesor", backref="grupos")
    estudiantes = relationship(
        "Estudiante",
        secondary=grupo_estudiante,
        backref="grupos",
    )

    def __repr__(self):
        return f"<Grupo(id_grupo={self.id_grupo}, nombre='{self.nombre}')>"

    periodo_id = Column(
        UUID(as_uuid=True), ForeignKey("periodos.id_periodo"), nullable=False
    )

    periodo = relationship("Periodo", back_populates="grupos")
