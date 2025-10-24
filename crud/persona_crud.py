from sqlalchemy.orm import Session
from models.persona import Persona
import uuid
from typing import List, Optional


def create_persona(db: Session, nombre: str, email: str, telefono: str) -> Persona:
    """
    Crea una nueva persona en la base de datos.
    """
    persona = Persona(nombre=nombre, email=email, telefono=telefono)
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


def get_persona_by_id(db: Session, persona_id: uuid.UUID) -> Optional[Persona]:
    """
    Obtiene una persona por su ID.
    """
    return db.query(Persona).filter(Persona.id_persona == persona_id).first()


def get_all_personas(db: Session) -> List[Persona]:
    """
    Devuelve todas las personas registradas.
    """
    return db.query(Persona).all()


def update_persona(
    db: Session,
    persona_id: uuid.UUID,
    nombre: Optional[str] = None,
    email: Optional[str] = None,
    telefono: Optional[str] = None,
) -> Optional[Persona]:
    """
    Actualiza los datos de una persona.
    """
    persona = db.query(Persona).filter(Persona.id_persona == persona_id).first()
    if persona is None:
        return None

    if nombre is not None:
        persona.nombre = nombre
    if email is not None:
        persona.email = email
    if telefono is not None:
        persona.telefono = telefono

    db.commit()
    db.refresh(persona)
    return persona


def delete_persona(db: Session, persona_id: uuid.UUID) -> bool:
    """
    Elimina una persona de la base de datos.
    """
    persona = db.query(Persona).filter(Persona.id_persona == persona_id).first()
    if persona is None:
        return False

    db.delete(persona)
    db.commit()
    return True
