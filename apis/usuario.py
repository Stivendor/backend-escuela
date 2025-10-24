from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import usuario_crud as crud_usuario
from migrations.schemas import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
)

router = APIRouter()


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    return crud_usuario.create_usuario(
        db,
        username=usuario.username,
        password=usuario.password,
        rol=usuario.rol,
        estudiante_id=usuario.estudiante_id,
        profesor_id=usuario.profesor_id,
    )


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios registrados.
    """
    return crud_usuario.get_all_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID único.
    """
    user = crud_usuario.get_usuario_by_id(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: str, usuario: UsuarioUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un usuario existente.
    """
    actualizado = crud_usuario.update_usuario(
        db,
        usuario_id=usuario_id,
        username=usuario.username,
        password=usuario.password,
        rol=usuario.rol,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    eliminado = crud_usuario.delete_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}


@router.post("/login")
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Autentica a un usuario con sus credenciales.
    """
    usuario = crud_usuario.autenticar_usuario(db, datos.username, datos.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"mensaje": "Login exitoso", "usuario_id": str(usuario.id_usuario)}
