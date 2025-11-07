from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import nota_crud as crud_nota
from migrations.schemas import NotaCreate, NotaUpdate, NotaResponse

router = APIRouter()


@router.post("/", response_model=NotaResponse)
def crear_nota(nota: NotaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva nota en la base de datos.
    """
    nueva = crud_nota.create_nota(
        db=db,
        estudiante_id=nota.estudiante_id,
        materia_id=nota.materia_id,
        valor=nota.valor,
    )
    return nueva


@router.get("/")
def listar_notas(db: Session = Depends(get_db)):
    """
    Lista todas las notas registradas, incluyendo los nombres de materia,
    estudiante y profesor.
    """
    return crud_nota.listar_notas(db)


@router.get("/{id_nota}", response_model=NotaResponse)
def obtener_nota(id_nota: str, db: Session = Depends(get_db)):
    """
    Obtiene una nota específica por su ID.
    """
    nota = db.query(crud_nota.Nota).filter(crud_nota.Nota.id_nota == id_nota).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota


@router.put("/{id_nota}", response_model=NotaResponse)
def actualizar_nota(id_nota: str, datos: NotaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el valor de una nota existente.
    """
    actualizada = crud_nota.actualizar_nota(
        db=db,
        id_nota=id_nota,
        valor=datos.valor,
    )
    if not actualizada:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return actualizada


@router.delete("/{id_nota}")
def eliminar_nota(id_nota: str, db: Session = Depends(get_db)):
    """
    Elimina una nota de la base de datos por ID.
    """
    eliminada = crud_nota.eliminar_nota(db, id_nota)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return {"mensaje": "Nota eliminada correctamente"}
