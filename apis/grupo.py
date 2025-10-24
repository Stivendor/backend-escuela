from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import grupo_crud as crud_grupo
from migrations.schemas import GrupoCreate, GrupoUpdate, GrupoResponse

router = APIRouter()


@router.post("/", response_model=GrupoResponse)
def crear_grupo(grupo: GrupoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo grupo con materia, profesor y periodo asociados.
    """
    nuevo = crud_grupo.create_grupo(
        db=db,
        nombre=grupo.nombre,
        materia_id=grupo.materia_id,
        profesor_id=grupo.profesor_id,
        periodo_id=grupo.periodo_id,
    )
    return nuevo


@router.get("/", response_model=list[GrupoResponse])
def listar_grupos(db: Session = Depends(get_db)):
    """
    Lista todos los grupos registrados.
    """
    return crud_grupo.get_all_grupos(db)


@router.get("/{grupo_id}", response_model=GrupoResponse)
def obtener_grupo(grupo_id: str, db: Session = Depends(get_db)):
    """
    Obtiene un grupo por su ID.
    """
    grupo = crud_grupo.get_grupo_by_id(db, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.put("/{grupo_id}", response_model=GrupoResponse)
def actualizar_grupo(grupo_id: str, datos: GrupoUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el nombre de un grupo.
    """
    actualizado = crud_grupo.update_grupo(
        db=db,
        grupo_id=grupo_id,
        nombre=datos.nombre,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return actualizado


@router.delete("/{grupo_id}")
def eliminar_grupo(grupo_id: str, db: Session = Depends(get_db)):
    """
    Elimina un grupo de la base de datos por ID.
    """
    eliminado = crud_grupo.delete_grupo(db, grupo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return {"mensaje": "Grupo eliminado correctamente"}
