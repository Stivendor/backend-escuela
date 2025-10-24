import uuid
from sqlalchemy.orm import Session
from models.materia import Materia
from models.profesor import Profesor


def create_materia(
    db: Session,
    nombre: str,
    codigo: str,
    creditos: int,
    profesor_id: uuid.UUID = None,
    usuario_id=None,
):
    materia = Materia(
        nombre=nombre, codigo=codigo, creditos=creditos, profesor_id=profesor_id
    )
    db.add(materia)
    db.commit()
    db.refresh(materia)

    if usuario_id:
        from models.auditoria import Auditoria

        auditoria = Auditoria(
            usuario_id=usuario_id, accion="Creación de materia", tabla="materias"
        )
        db.add(auditoria)
        db.commit()

    return materia


def listar_materias(db: Session):
    materias = db.query(Materia).all()
    for m in materias:
        profesor_nombre = (
            m.profesor.persona.nombre if m.profesor else "Sin profesor asignado"
        )
        print(
            f"""
        ID: {m.id_materia}
        Nombre: {m.nombre}
        Código: {m.codigo}
        Créditos: {m.creditos}
        Profesor: {profesor_nombre}
        """
        )
    return materias


def actualizar_materia(
    db: Session,
    materia_id: uuid.UUID,
    nombre: str = None,
    codigo: str = None,
    creditos: int = None,
    profesor_id: uuid.UUID = None,
):
    materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()
    if not materia:
        print("No se encontró ninguna materia con ese ID.")
        return None

    if nombre:
        materia.nombre = nombre
    if codigo is not None and codigo != "":
        materia.codigo = codigo
    if creditos is not None:
        materia.creditos = creditos

    db.commit()
    db.refresh(materia)
    return materia


def eliminar_materia(db: Session, materia_id: uuid.UUID):
    materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()
    if materia:
        db.delete(materia)
        db.commit()
        return materia
    else:
        print("No se encontró ninguna materia con ese ID.")
        return None
