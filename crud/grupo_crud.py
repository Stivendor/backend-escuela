from sqlalchemy.orm import Session
from models.grupo import Grupo
import uuid
from typing import List, Optional


def create_grupo(
    db: Session,
    nombre: str,
    materia_id: uuid.UUID,
    profesor_id: uuid.UUID,
    periodo_id: uuid.UUID,
) -> Grupo:

    grupo = Grupo(
        nombre=nombre,
        materia_id=materia_id,
        profesor_id=profesor_id,
        periodo_id=periodo_id,
    )
    db.add(grupo)
    db.commit()
    db.refresh(grupo)
    return grupo


def get_grupo_by_id(db: Session, grupo_id: uuid.UUID) -> Optional[Grupo]:

    return db.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()


def get_all_grupos(db: Session) -> List[Grupo]:

    return db.query(Grupo).all()


def update_grupo(
    db: Session, grupo_id: uuid.UUID, nombre: Optional[str] = None
) -> Optional[Grupo]:

    grupo = db.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()
    if grupo is None:
        return None

    if nombre is not None:
        grupo.nombre = nombre

    db.commit()
    db.refresh(grupo)
    return grupo


def delete_grupo(db: Session, grupo_id: uuid.UUID) -> bool:

    grupo = db.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()
    if grupo is None:
        return False

    db.delete(grupo)
    db.commit()
    return True
