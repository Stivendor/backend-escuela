import uuid
from sqlalchemy.orm import Session
from models.persona import Persona
from models.estudiante import Estudiante
from sqlalchemy.orm import joinedload


def create_estudiante(
    db: Session,
    nombre: str,
    email: str,
    telefono: str,
    carrera: str,
    semestre: int,
    usuario_id=None,
):
    persona = Persona(nombre=nombre, email=email, telefono=telefono)
    db.add(persona)
    db.commit()
    db.refresh(persona)

    estudiante = Estudiante(
        persona_id=persona.id_persona, carrera=carrera, semestre=semestre
    )
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)

    if usuario_id:
        from models.auditoria import Auditoria

        auditoria = Auditoria(
            usuario_id=usuario_id, accion="Creación de estudiante", tabla="estudiantes"
        )
        db.add(auditoria)
        db.commit()

    return estudiante


def listar_estudiantes(db: Session):
    return db.query(Estudiante).options(joinedload(Estudiante.persona)).all()


def actualizar_estudiante(
    db: Session,
    estudiante_id: uuid.UUID,
    nombre: str = None,
    email: str = None,
    telefono: str = None,
    carrera: str = None,
    semestre: int = None,
    usuario_id=None,
):
    estudiante = (
        db.query(Estudiante).filter(Estudiante.id_estudiante == estudiante_id).first()
    )
    if estudiante:
        persona = db.query(Persona).filter(Persona.id_persona == estudiante.persona_id).first()
        if persona:
            if nombre is not None:
                persona.nombre = nombre
            if email is not None:
                persona.email = email
            if telefono is not None:
                persona.telefono = telefono

        if carrera is not None:
            estudiante.carrera = carrera
        if semestre is not None:
            estudiante.semestre = semestre

        db.commit()
        db.refresh(estudiante)

        if usuario_id:
            from models.auditoria import Auditoria

            auditoria = Auditoria(
                usuario_id=usuario_id,
                accion="Actualización de estudiante",
                tabla="estudiantes",
            )
            db.add(auditoria)
            db.commit()

    return estudiante


def eliminar_estudiante(db: Session, estudiante_id: uuid.UUID, usuario_id=None):
    estudiante = (
        db.query(Estudiante).filter(Estudiante.id_estudiante == estudiante_id).first()
    )
    if estudiante:
        db.delete(estudiante)
        db.commit()

        if usuario_id:
            from models.auditoria import Auditoria

            auditoria = Auditoria(
                usuario_id=usuario_id,
                accion="Eliminación de estudiante",
                tabla="estudiantes",
            )
            db.add(auditoria)
            db.commit()

    return estudiante

def get_estudiante_by_id(db: Session, estudiante_id: uuid.UUID):
    """
    Obtiene un estudiante por su ID, incluyendo los datos de la persona asociada.
    """
    return (
        db.query(Estudiante)
        .options(joinedload(Estudiante.persona))
        .filter(Estudiante.id_estudiante == estudiante_id)
        .first()
    )
