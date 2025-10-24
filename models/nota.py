import uuid
from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Nota(Base):
    __tablename__ = "notas"

    id_nota = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    estudiante_id = Column(
        UUID(as_uuid=True), ForeignKey("estudiantes.id_estudiante"), nullable=False
    )
    profesor_id = Column(
        UUID(as_uuid=True), ForeignKey("profesores.id_profesor"), nullable=True
    )
    materia_id = Column(
        UUID(as_uuid=True), ForeignKey("materias.id_materia"), nullable=False
    )

    valor = Column(Float, nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    estudiante = relationship("Estudiante", backref="notas")
    profesor = relationship("Profesor", backref="notas")
    materia = relationship("Materia", back_populates="notas")

    def __repr__(self):
        return f"<Nota(id_nota={self.id_nota}, estudiante_id={self.estudiante_id}, materia_id={self.materia_id}, valor={self.valor})>"
