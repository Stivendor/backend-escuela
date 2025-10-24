from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from crud import periodo_crud as crud_periodo
from migrations.schemas import PeriodoCreate, PeriodoUpdate, PeriodoResponse

router = APIRouter()


@router.post("/", response_model=PeriodoResponse)
def crear_periodo(periodo: PeriodoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo periodo académico con nombre, fecha inicio y fecha fin.
    """
    nuevo = crud_periodo.create_periodo(
        db=db,
        nombre=periodo.nombre,
        fecha_inicio=periodo.fecha_inicio,
        fecha_fin=periodo.fecha_fin,
    )
    return nuevo


@router.get("/", response_model=list[PeriodoResponse])
def listar_periodos(db: Session = Depends(get_db)):
    """
    Lista todos los periodos académicos.
    """
    return crud_periodo.get_all_periodos(db)


@router.get("/{periodo_id}", response_model=PeriodoResponse)
def obtener_periodo(periodo_id: str, db: Session = Depends(get_db)):
    """
    Obtiene un periodo por su ID.
    """
    periodo = crud_periodo.get_periodo_by_id(db, periodo_id)
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo


@router.put("/{periodo_id}", response_model=PeriodoResponse)
def actualizar_periodo(
    periodo_id: str, datos: PeriodoUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un periodo académico.
    """
    actualizado = crud_periodo.update_periodo(
        db=db,
        periodo_id=periodo_id,
        nombre=datos.nombre,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return actualizado


@router.delete("/{periodo_id}")
def eliminar_periodo(periodo_id: str, db: Session = Depends(get_db)):
    """
    Elimina un periodo académico por ID.
    """
    eliminado = crud_periodo.delete_periodo(db, periodo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return {"mensaje": "Periodo eliminado correctamente"}
