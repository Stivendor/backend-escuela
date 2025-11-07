from sqlalchemy.orm import Session, joinedload
from models.nota import Nota
from models.estudiante import Estudiante
from models.profesor import Profesor
from models.materia import Materia
from models.persona import Persona


def create_nota(db: Session, estudiante_id: str, materia_id: str, valor: float):
    """
    Crea una nueva nota en la base de datos.
    """
    nueva_nota = Nota(estudiante_id=estudiante_id, materia_id=materia_id, valor=valor)
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota


def listar_notas(db: Session):
    """
    Lista todas las notas incluyendo los nombres de materia, estudiante y profesor.
    """
    notas = (
        db.query(Nota)
        .options(
            joinedload(Nota.materia).joinedload(Materia.profesor).joinedload(Profesor.persona),
            joinedload(Nota.estudiante).joinedload(Estudiante.persona)
        )
        .all()
    )

    resultado = []
    for n in notas:
        resultado.append({
            "id_nota": n.id_nota,
            "valor": n.valor,
            "fecha_creacion": n.fecha_creacion,

            # Materia
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else "Sin materia",

            # Estudiante
            "estudiante_id": n.estudiante_id,
            "estudiante_nombre": (
                n.estudiante.persona.nombre
                if n.estudiante and n.estudiante.persona
                else "Sin estudiante"
            ),

            # Profesor
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


def actualizar_nota(db: Session, id_nota: str, valor: float = None):
    """
    Actualiza el valor de una nota existente.
    """
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()
    if nota:
        if valor is not None:
            nota.valor = valor
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
