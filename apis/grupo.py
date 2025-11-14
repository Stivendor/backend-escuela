from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database.config import get_db
from crud import grupo_crud as crud_grupo
from migrations.schemas import GrupoCreate, GrupoUpdate, GrupoResponse

# 👇 IMPORTANTE: SIN prefix aquí, el prefix lo pone main.py
router = APIRouter()


@router.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def crear_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo grupo con materia y profesor asociados.
    El campo periodo_id es opcional.
    """
    nuevo = crud_grupo.create_grupo(
        db=db,
        nombre=grupo.nombre,
        materia_id=grupo.materia_id,
        profesor_id=grupo.profesor_id,
        periodo_id=grupo.periodo_id,  # puede ser None
    )
    return nuevo


@router.get("/", response_model=list[GrupoResponse])
def listar_grupos(db: Session = Depends(get_db)):
    """
    Lista todos los grupos registrados.
    """
    return crud_grupo.get_all_grupos(db)


@router.get("/{grupo_id}", response_model=GrupoResponse)
def obtener_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene un grupo por su ID.
    """
    grupo = crud_grupo.get_grupo_by_id(db, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.put("/{grupo_id}", response_model=GrupoResponse)
def actualizar_grupo(grupo_id: UUID, datos: GrupoUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un grupo.
    """
    actualizado = crud_grupo.update_grupo(
        db=db,
        grupo_id=grupo_id,
        nombre=datos.nombre,
        materia_id=datos.materia_id,
        profesor_id=datos.profesor_id,
        periodo_id=datos.periodo_id,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return actualizado


@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un grupo de la base de datos por ID.
    """
    eliminado = crud_grupo.delete_grupo(db, grupo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return
