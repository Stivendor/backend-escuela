from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from models.auditoria import Auditoria
from migrations.schemas import AuditoriaResponse

router = APIRouter()


@router.get("/", response_model=list[AuditoriaResponse])
def listar_auditorias(db: Session = Depends(get_db)):
    """
    Lista todos los registros de auditoría ordenados por fecha descendente.
    """
    return db.query(Auditoria).order_by(Auditoria.fecha.desc()).all()


@router.get("/usuario/{usuario_id}", response_model=list[AuditoriaResponse])
def auditorias_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """
    Lista los registros de auditoría de un usuario específico.
    """
    registros = (
        db.query(Auditoria)
        .filter(Auditoria.usuario_id == usuario_id)
        .order_by(Auditoria.fecha.desc())
        .all()
    )
    if not registros:
        raise HTTPException(
            status_code=404, detail="No se encontraron auditorías para este usuario"
        )
    return registros
