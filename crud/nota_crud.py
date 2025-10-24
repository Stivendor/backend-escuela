import uuid
from sqlalchemy.orm import Session
from models.nota import Nota


def create_nota(db: Session, estudiante_id: str, materia_id: str, valor: float):
    nueva_nota = Nota(estudiante_id=estudiante_id, materia_id=materia_id, valor=valor)
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota


def listar_notas(db: Session):
    return db.query(Nota).all()


def actualizar_nota(db: Session, id_nota: str, valor: float = None):
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if nota:
        if valor is not None:
            nota.valor = valor
        db.commit()
        db.refresh(nota)
    return nota


def eliminar_nota(db: Session, id_nota: str):
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if nota:
        db.delete(nota)
        db.commit()
    return nota
