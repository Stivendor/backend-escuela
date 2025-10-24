from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import persona_crud as crud_persona
from migrations.schemas import PersonaCreate, PersonaUpdate, PersonaResponse

router = APIRouter()


@router.post("/", response_model=PersonaResponse)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva persona.
    """
    return crud_persona.create_persona(
        db, persona.nombre, persona.email, persona.telefono
    )


@router.get("/", response_model=list[PersonaResponse])
def listar_personas(db: Session = Depends(get_db)):
    """
    Lista todas las personas.
    """
    return crud_persona.get_all_personas(db)


@router.get("/{persona_id}", response_model=PersonaResponse)
def obtener_persona(persona_id: str, db: Session = Depends(get_db)):
    """
    Obtiene una persona por ID.
    """
    persona = crud_persona.get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@router.put("/{persona_id}", response_model=PersonaResponse)
def actualizar_persona(
    persona_id: str, datos: PersonaUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una persona.
    """
    actualizada = crud_persona.update_persona(
        db, persona_id, datos.nombre, datos.email, datos.telefono
    )
    if not actualizada:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return actualizada


@router.delete("/{persona_id}")
def eliminar_persona(persona_id: str, db: Session = Depends(get_db)):
    """
    Elimina una persona de la base de datos.
    """
    eliminada = crud_persona.delete_persona(db, persona_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"mensaje": "Persona eliminada correctamente"}
