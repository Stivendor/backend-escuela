from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import profesor_crud as crud_profesor
from migrations.schemas import ProfesorCreate, ProfesorUpdate, ProfesorResponse
from models.profesor import Profesor

router = APIRouter()


@router.post("/", response_model=ProfesorResponse)
def crear_profesor(profesor: ProfesorCreate, db: Session = Depends(get_db)):
    """Crea un nuevo profesor junto con su persona asociada."""
    nuevo = crud_profesor.create_profesor(
        db=db,
        nombre=profesor.nombre,
        email=profesor.email,
        telefono=profesor.telefono,
        especialidad=profesor.especialidad,
        usuario_id=profesor.usuario_id,
    )
    return nuevo


@router.get("/", response_model=list[ProfesorResponse])
def listar_profesores(db: Session = Depends(get_db)):
    """Lista todos los profesores registrados."""
    return crud_profesor.listar_profesores(db)


@router.get("/{profesor_id}", response_model=ProfesorResponse)
def obtener_profesor(profesor_id: str, db: Session = Depends(get_db)):
    """Obtiene un profesor por su ID único."""
    profesor = db.query(Profesor).filter(Profesor.id_profesor == profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor


@router.put("/{profesor_id}", response_model=ProfesorResponse)
def actualizar_profesor(
    profesor_id: str, datos: ProfesorUpdate, db: Session = Depends(get_db)
):
    """Actualiza los datos de un profesor y de su persona asociada."""
    actualizado = crud_profesor.actualizar_profesor(
        db=db,
        profesor_id=profesor_id,
        nuevo_nombre=datos.nombre,
        nuevo_email=datos.email,
        nuevo_telefono=datos.telefono,
        nueva_especialidad=datos.especialidad,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return actualizado


@router.delete("/{profesor_id}")
def eliminar_profesor(profesor_id: str, db: Session = Depends(get_db)):
    """Elimina un profesor si no tiene un usuario asociado."""
    try:
        eliminado = crud_profesor.eliminar_profesor(db, profesor_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
        return {"mensaje": "Profesor eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
