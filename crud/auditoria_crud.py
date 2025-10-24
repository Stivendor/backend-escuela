from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from models.auditoria import Auditoria


def create_auditoria(
    db: Session, usuario_id: uuid.UUID | None, accion: str, tabla: str
):

    auditoria = Auditoria(usuario_id=usuario_id, accion=accion, tabla=tabla)
    db.add(auditoria)
    db.commit()
    db.refresh(auditoria)


def get_auditoria(db: Session) -> List[Auditoria]:
    return db.query(Auditoria).all()


def ver_auditoria(db):
    auditorias = db.query(Auditoria).order_by(Auditoria.fecha.desc()).all()
    if not auditorias:
        print(" No hay registros de auditoría.")
        return

    print("\n=== REGISTRO DE AUDITORÍA ===")
    for a in auditorias:
        print(
            f"[{a.fecha.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Usuario ID: {a.usuario_id} | "
            f"Tabla: {a.tabla} | "
            f"Acción: {a.accion}"
        )
    print("==============================\n")
