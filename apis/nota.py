from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import nota_crud as crud_nota
from migrations.schemas import NotaCreate, NotaUpdate, NotaResponse

router = APIRouter()


@router.get("/", response_model=list[NotaResponse])
def listar_notas(db: Session = Depends(get_db)):
    """
    Lista todas las notas.
    """
    return crud_nota.listar_notas(db)



@router.post("/", response_model=NotaResponse)
def crear_nota(nota: NotaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva nota en la base de datos.
    """
    nueva_nota = crud_nota.create_nota(
        db,
        estudiante_id=nota.estudiante_id,
        materia_id=nota.materia_id,
        profesor_id=nota.profesor_id,  # ✅ se pasa al CRUD
        valor=nota.valor
    )
    return nueva_nota


@router.put("/{id_nota}", response_model=NotaResponse)
def actualizar_nota(id_nota: str, nota: NotaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los campos de una nota existente.
    """
    actualizada = crud_nota.actualizar_nota(
        db=db,
        id_nota=id_nota,
        valor=nota.valor,
        materia_id=nota.materia_id,
        estudiante_id=nota.estudiante_id,
        profesor_id=nota.profesor_id
    )
    if not actualizada:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return actualizada


@router.delete("/{id_nota}")
def eliminar_nota(id_nota: str, db: Session = Depends(get_db)):
    """
    Elimina una nota existente.
    """
    eliminada = crud_nota.eliminar_nota(db, id_nota)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return {"mensaje": "Nota eliminada correctamente"}
