import uuid
from database.config import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Profesor(Base):
    __tablename__ = "profesores"

    id_profesor = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(
        UUID(as_uuid=True),
        ForeignKey("personas.id_persona", ondelete="CASCADE"),
        nullable=False,
    )
    especialidad = Column(String(100), nullable=False)

    persona = relationship("Persona", backref="profesor")
