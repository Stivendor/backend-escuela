import uuid
from database.config import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Periodo(Base):
    __tablename__ = "periodos"

    id_periodo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    grupos = relationship("Grupo", back_populates="periodo")

    def __repr__(self):
        return f"<Periodo(id_periodo={self.id_periodo}, nombre='{self.nombre}')>"
