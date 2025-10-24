import uuid
from database.config import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id_estudiante = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(
        UUID(as_uuid=True),
        ForeignKey("personas.id_persona", ondelete="CASCADE"),
        nullable=False,
    )
    carrera = Column(String(100), nullable=False)
    semestre = Column(Integer, nullable=False)

    persona = relationship("Persona", backref="estudiante")
