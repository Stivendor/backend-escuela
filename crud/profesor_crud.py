import uuid
from sqlalchemy.orm import Session, joinedload
from models.persona import Persona
from models.profesor import Profesor
from models.usuarios import Usuario


def create_profesor(
    db: Session,
    nombre: str,
    email: str,
    telefono: str,
    especialidad: str,
    usuario_id=None,
):
    # Crear persona primero
    persona = Persona(nombre=nombre, email=email, telefono=telefono)
    db.add(persona)
    db.commit()
    db.refresh(persona)

    # Crear profesor asociado
    profesor = Profesor(persona_id=persona.id_persona, especialidad=especialidad)
    db.add(profesor)
    db.commit()
    db.refresh(profesor)

    # Registrar auditoría si aplica
    if usuario_id:
        from models.auditoria import Auditoria
        auditoria = Auditoria(
            usuario_id=usuario_id,
            accion="Creación de profesor",
            tabla="profesores",
        )
        db.add(auditoria)
        db.commit()

    return profesor


def listar_profesores(db: Session):
    """Lista todos los profesores con su persona asociada."""
    return db.query(Profesor).options(joinedload(Profesor.persona)).all()


def actualizar_profesor(
    db: Session,
    profesor_id: uuid.UUID,
    nuevo_nombre: str = None,
    nuevo_email: str = None,
    nuevo_telefono: str = None,
    nueva_especialidad: str = None,
):
    profesor = db.query(Profesor).filter(Profesor.id_profesor == profesor_id).first()
    if profesor:
        persona = db.query(Persona).filter(Persona.id_persona == profesor.persona_id).first()
        if persona:
            if nuevo_nombre:
                persona.nombre = nuevo_nombre
            if nuevo_email:
                persona.email = nuevo_email
            if nuevo_telefono:
                persona.telefono = nuevo_telefono

        if nueva_especialidad:
            profesor.especialidad = nueva_especialidad

        db.commit()
        db.refresh(profesor)
        return profesor
    return None


def eliminar_profesor(db: Session, profesor_id: uuid.UUID):
    """
    Elimina un profesor si no tiene un usuario asociado.
    Si existe un usuario vinculado, lanza una excepción controlada.
    """
    profesor = db.query(Profesor).filter(Profesor.id_profesor == profesor_id).first()
    if not profesor:
        return None

    # Verificar si hay usuario vinculado
    usuario = db.query(Usuario).filter(Usuario.profesor_id == profesor_id).first()
    if usuario:
        raise Exception("No se puede eliminar: el profesor tiene un usuario asociado.")

    db.delete(profesor)
    db.commit()
    return profesor
