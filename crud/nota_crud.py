from sqlalchemy.orm import Session, joinedload
from models.nota import Nota
from models.estudiante import Estudiante
from models.profesor import Profesor
from models.materia import Materia
from models.persona import Persona
from sqlalchemy import func


def create_nota(db: Session, estudiante_id: str, materia_id: str, valor: float, profesor_id: str = None):
    """
    Crea una nueva nota en la base de datos.
    """
    nueva_nota = Nota(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        profesor_id=profesor_id,  # ✅ ahora lo guarda correctamente
        valor=valor
    )
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota



def listar_notas(db: Session, materia: str | None = None, estudiante: str | None = None):
    """
    Lista todas las notas con nombres de materia, estudiante y profesor.
    Permite filtrar por materia o estudiante.
    """
    query = (
        db.query(Nota)
        .options(
            joinedload(Nota.materia).joinedload(Materia.profesor).joinedload(Profesor.persona),
            joinedload(Nota.estudiante).joinedload(Estudiante.persona)
        )
    )

    # 🔍 Filtros opcionales
    if materia and materia.strip():
        query = query.join(Materia).filter(func.lower(Materia.nombre).ilike(f"%{materia.lower()}%"))

    if estudiante and estudiante.strip():
        query = query.join(Estudiante).join(Persona).filter(
            func.lower(Persona.nombre).ilike(f"%{estudiante.lower()}%")
        )

    notas = query.all()

    resultado = []
    for n in notas:
        resultado.append({
            "id_nota": n.id_nota,
            "valor": n.valor,
            "fecha_creacion": n.fecha_creacion,

            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else "Sin materia",

            "estudiante_id": n.estudiante_id,
            "estudiante_nombre": (
                n.estudiante.persona.nombre
                if n.estudiante and n.estudiante.persona
                else "Sin estudiante"
            ),

            "profesor_id": (
                n.materia.profesor_id
                if n.materia and n.materia.profesor_id
                else None
            ),
            "profesor_nombre": (
                n.materia.profesor.persona.nombre
                if n.materia and n.materia.profesor and n.materia.profesor.persona
                else "Sin profesor asignado"
            ),
        })

    return resultado

def actualizar_nota(
    db: Session,
    id_nota: str,
    valor: float = None,
    materia_id: str = None,
    estudiante_id: str = None,
    profesor_id: str = None,
):
    """
    Actualiza los campos de una nota existente.
    """
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if not nota:
        return None

    if valor is not None:
        nota.valor = valor
    if materia_id is not None:
        nota.materia_id = materia_id
    if estudiante_id is not None:
        nota.estudiante_id = estudiante_id
    if profesor_id is not None:
        nota.profesor_id = profesor_id

    db.commit()
    db.refresh(nota)
    return nota


def eliminar_nota(db: Session, id_nota: str):
    """
    Elimina una nota por ID.
    """
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if nota:
        db.delete(nota)
        db.commit()
    return nota
