from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import materia_crud as crud_materia
from migrations.schemas import MateriaCreate, MateriaUpdate, MateriaResponse

router = APIRouter()


@router.post("/", response_model=MateriaResponse)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva materia en la base de datos.
    Registra auditoría si se envía usuario_id.
    """
    nueva = crud_materia.create_materia(
        db=db,
        nombre=materia.nombre,
        codigo=materia.codigo,
        creditos=materia.creditos,
        profesor_id=materia.profesor_id,
        usuario_id=materia.usuario_id,
    )
    return nueva


@router.get("/", response_model=list[MateriaResponse])
def listar_materias(nombre: str | None = None, db: Session = Depends(get_db)):
    """
    Lista todas las materias registradas.
    Si se envía el parámetro 'nombre', filtra por coincidencia parcial.
    """
    return crud_materia.listar_materias(db, nombre)



@router.get("/{materia_id}", response_model=MateriaResponse)
def obtener_materia(materia_id: str, db: Session = Depends(get_db)):
    """
    Obtiene una materia específica por su ID.
    """
    materia = (
        db.query(crud_materia.Materia)
        .filter(crud_materia.Materia.id_materia == materia_id)
        .first()
    )
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.put("/{materia_id}", response_model=MateriaResponse)
def actualizar_materia(
    materia_id: str, datos: MateriaUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una materia existente.
    """
    actualizada = crud_materia.actualizar_materia(
        db=db,
        materia_id=materia_id,
        nombre=datos.nombre,
        codigo=datos.codigo,
        creditos=datos.creditos,
        profesor_id=datos.profesor_id,
    )
    if not actualizada:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return actualizada


@router.delete("/{materia_id}")
def eliminar_materia(materia_id: str, db: Session = Depends(get_db)):
    """
    Elimina una materia de la base de datos por ID.
    """
    eliminada = crud_materia.eliminar_materia(db, materia_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return {"mensaje": "Materia eliminada correctamente"}
