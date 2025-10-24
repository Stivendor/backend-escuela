import uuid
from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Auditoria(Base):
    __tablename__ = "auditorias"

    id_auditoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    usuario_id = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    accion = Column(String(100), nullable=False)
    tabla = Column(String(50), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", backref="auditorias")

    def __repr__(self):
        return f"<Auditoria(usuario_id={self.usuario_id}, accion='{self.accion}', tabla='{self.tabla}')>"
