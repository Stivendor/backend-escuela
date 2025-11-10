from sqlalchemy.orm import Session, joinedload
from models.nota import Nota
from models.estudiante import Estudiante
from models.profesor import Profesor
from models.materia import Materia
from models.persona import Persona


def create_nota(db: Session, estudiante_id: str, materia_id: str, valor: float):
    """
    Crea una nueva nota en la base de datos.
    Si la materia tiene un profesor asignado, se guarda automáticamente.
    """
    # 🔹 Buscar el profesor de la materia seleccionada
    materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()

    profesor_id = materia.profesor_id if materia and materia.profesor_id else None

    nueva_nota = Nota(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        profesor_id=profesor_id,  # ✅ se asigna automáticamente
        valor=valor
    )

    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota


def listar_notas(db: Session):
    """
    Lista todas las notas incluyendo los nombres de materia, estudiante y profesor.
    Usa joinedload para optimizar las consultas y evita ciclos de referencia.
    """
    notas = (
        db.query(Nota)
        .options(
            joinedload(Nota.materia)
            .joinedload(Materia.profesor)
            .joinedload(Profesor.persona),
            joinedload(Nota.estudiante).joinedload(Estudiante.persona),
        )
        .all()
    )

    resultado = []
    for n in notas:
        materia = n.materia
        estudiante = n.estudiante
        profesor = materia.profesor if materia else None
        persona_prof = profesor.persona if profesor else None

        resultado.append({
            "id_nota": n.id_nota,
            "valor": n.valor,
            "fecha_creacion": n.fecha_creacion,

            "materia_id": materia.id_materia if materia else None,
            "materia_nombre": materia.nombre if materia else "Sin materia",

            "estudiante_id": estudiante.id_estudiante if estudiante else None,
            "estudiante_nombre": (
                estudiante.persona.nombre
                if estudiante and estudiante.persona
                else "Sin estudiante"
            ),

            "profesor_id": profesor.id_profesor if profesor else None,
            "profesor_nombre": (
                persona_prof.nombre
                if persona_prof
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
    activo: bool = None,
):
    """
    Actualiza los campos de una nota existente (valor, materia, estudiante, profesor, activo).
    Si se cambia la materia, actualiza automáticamente el profesor asociado.
    """
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if not nota:
        return None

    if valor is not None:
        nota.valor = valor

    if materia_id is not None:
        nota.materia_id = materia_id
        # 🔹 Si la materia tiene profesor, se actualiza automáticamente
        materia = db.query(Materia).filter(Materia.id_materia == materia_id).first()
        if materia and materia.profesor_id:
            nota.profesor_id = materia.profesor_id

    if estudiante_id is not None:
        nota.estudiante_id = estudiante_id

    if profesor_id is not None:
        nota.profesor_id = profesor_id

    if activo is not None:
        nota.activo = activo

    db.commit()
    db.refresh(nota)
    return nota


def eliminar_nota(db: Session, id_nota: str):
    """
    Elimina una nota de la base de datos por ID.
    """
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if nota:
        db.delete(nota)
        db.commit()
    return nota
