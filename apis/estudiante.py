from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import estudiante_crud as crud_estudiante
from migrations.schemas import EstudianteCreate, EstudianteUpdate, EstudianteResponse

router = APIRouter()


@router.post("/", response_model=EstudianteResponse)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo estudiante con su persona asociada.
    También registra la acción en auditoría si se envía usuario_id.
    """
    nuevo = crud_estudiante.create_estudiante(
        db=db,
        nombre=estudiante.nombre,
        email=estudiante.email,
        telefono=estudiante.telefono,
        carrera=estudiante.carrera,
        semestre=estudiante.semestre,
        usuario_id=estudiante.usuario_id,
    )
    return nuevo


@router.get("/", response_model=list[EstudianteResponse])
def listar_estudiantes(db: Session = Depends(get_db)):
    """
    Lista todos los estudiantes, incluyendo los datos de Persona.
    """
    return crud_estudiante.listar_estudiantes(db)


@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(estudiante_id: str, db: Session = Depends(get_db)):
    """
    Obtiene un estudiante específico por su ID.
    """
    estudiante = crud_estudiante.get_estudiante_by_id(db, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: str, datos: EstudianteUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un estudiante y su persona asociada.
    """
    actualizado = crud_estudiante.actualizar_estudiante(
        db=db,
        estudiante_id=estudiante_id,
        nombre=datos.nombre,
        email=datos.email,
        telefono=datos.telefono,
        carrera=datos.carrera,
        semestre=datos.semestre,
        usuario_id=datos.usuario_id,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return actualizado


@router.delete("/{estudiante_id}")
def eliminar_estudiante(
    estudiante_id: str, usuario_id: str = None, db: Session = Depends(get_db)
):
    """
    Elimina un estudiante de la base de datos por ID.
    También registra la acción en auditoría si se envía usuario_id.
    """
    eliminado = crud_estudiante.eliminar_estudiante(
        db, estudiante_id, usuario_id=usuario_id
    )
    if not eliminado:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"mensaje": "Estudiante eliminado correctamente"}
