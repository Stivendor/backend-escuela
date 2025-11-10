import uuid
from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 🔹 Tabla intermedia para relación muchos-a-muchos entre materias y estudiantes
materia_estudiante = Table(
    "materia_estudiante",
    Base.metadata,
    Column(
        "materia_id",
        UUID(as_uuid=True),
        ForeignKey("materias.id_materia", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "estudiante_id",
        UUID(as_uuid=True),
        ForeignKey("estudiantes.id_estudiante", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Materia(Base):
    __tablename__ = "materias"

    id_materia = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    creditos = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    profesor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("profesores.id_profesor", ondelete="SET NULL"),  # ✅ mejor manejo si se borra el profe
        nullable=True,
    )

    # 🔹 Relación bidireccional con Profesor
    profesor = relationship("Profesor", back_populates="materias")

    # 🔹 Relación muchos-a-muchos con Estudiante
    estudiantes = relationship(
    "Estudiante",
    secondary="materia_estudiante",
    back_populates="materias"  # 👈 CAMBIO AQUÍ
)


    # 🔹 Relación uno-a-muchos con Nota
    notas = relationship("Nota", back_populates="materia", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Materia(id_materia={self.id_materia}, nombre='{self.nombre}', "
            f"codigo='{self.codigo}', creditos={self.creditos})>"
        )

