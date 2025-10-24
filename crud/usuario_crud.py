from sqlalchemy.orm import Session
from typing import List, Optional
from models.usuarios import Usuario
from models.auditoria import Auditoria


def create_usuario(
    db: Session,
    username: str,
    password: str,
    rol: str,
    estudiante_id: Optional[int] = None,
    profesor_id: Optional[int] = None,
) -> Usuario:
    usuario = Usuario(
        username=username,
        password=password,
        rol=rol,
        estudiante_id=estudiante_id,
        profesor_id=profesor_id,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def get_usuario_by_id(db: Session, usuario_id: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()


def get_all_usuarios(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()


def update_usuario(
    db: Session,
    usuario_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    rol: Optional[str] = None,
) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        return None

    if username is not None:
        usuario.username = username
    if password is not None:
        usuario.password = password
    if rol is not None:
        usuario.rol = rol

    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, usuario_id: str) -> bool:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        return False

    db.delete(usuario)
    db.commit()
    return True


def autenticar_usuario(db: Session, username: str, password: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario and usuario.password == password:
        auditoria = Auditoria(
            usuario_id=usuario.id_usuario, accion="Login exitoso", tabla="usuarios"
        )
        db.add(auditoria)
        db.commit()
        return usuario
    return None
