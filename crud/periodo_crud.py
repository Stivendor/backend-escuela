from sqlalchemy.orm import Session
from models.periodo import Periodo
import uuid
from typing import List, Optional
from datetime import date


def create_periodo(
    db: Session, nombre: str, fecha_inicio: date, fecha_fin: date
) -> Periodo:

    periodo = Periodo(nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    db.add(periodo)
    db.commit()
    db.refresh(periodo)
    return periodo


def get_periodo_by_id(db: Session, periodo_id: uuid.UUID) -> Optional[Periodo]:

    return db.query(Periodo).filter(Periodo.id_periodo == periodo_id).first()


def get_all_periodos(db: Session) -> List[Periodo]:

    return db.query(Periodo).all()


def update_periodo(
    db: Session,
    periodo_id: uuid.UUID,
    nombre: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
) -> Optional[Periodo]:

    periodo = db.query(Periodo).filter(Periodo.id_periodo == periodo_id).first()
    if periodo is None:
        return None

    if nombre is not None:
        periodo.nombre = nombre
    if fecha_inicio is not None:
        periodo.fecha_inicio = fecha_inicio
    if fecha_fin is not None:
        periodo.fecha_fin = fecha_fin

    db.commit()
    db.refresh(periodo)
    return periodo


def delete_periodo(db: Session, periodo_id: uuid.UUID) -> bool:

    periodo = db.query(Periodo).filter(Periodo.id_periodo == periodo_id).first()
    if periodo is None:
        return False

    db.delete(periodo)
    db.commit()
    return True
