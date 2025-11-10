"""
Schemas Pydantic para la API
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import date


"""
    Schemas para Persona
"""


# ==================== PERSONA ====================
class PersonaBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str


class PersonaCreate(PersonaBase):
    """
    Schema para crear persona.
    """

    pass


class PersonaUpdate(BaseModel):
    """
    Schema para actualizar persona (campos opcionales).
    """

    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


class PersonaResponse(PersonaBase):
    """
    Schema de respuesta con metadatos.
    """

    id_persona: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioBase(BaseModel):
    """
    Schema base para Usuario.
    Contiene los campos principales compartidos por creación, actualización y respuesta.
    """

    username: str
    rol: str
    estudiante_id: Optional[UUID] = None
    profesor_id: Optional[UUID] = None


class UsuarioCreate(UsuarioBase):
    """
    Schema para la creación de un nuevo usuario.
    Incluye la contraseña como campo obligatorio.
    """

    password: str


class UsuarioUpdate(BaseModel):
    """
    Schema para actualizar un usuario.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """

    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    estudiante_id: Optional[UUID] = None
    profesor_id: Optional[UUID] = None


class UsuarioResponse(UsuarioBase):
    """
    Schema de respuesta para Usuario.
    Incluye el ID y la fecha de creación.
    """

    id_usuario: UUID
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """
    Schema para autenticación de usuario (login).
    """

    username: str
    password: str


# ==================== ESTUDIANTE ====================
class EstudianteBase(BaseModel):
    """
    Schema base para Estudiante.
    """

    carrera: str
    semestre: int


class EstudianteCreate(PersonaBase, EstudianteBase):
    """
    Schema para la creación de un Estudiante.
    Incluye también los datos de Persona.
    """

    usuario_id: Optional[UUID] = None


class EstudianteUpdate(BaseModel):
    """
    Schema para actualizar un Estudiante.
    Todos los campos son opcionales.
    """

    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    usuario_id: Optional[UUID] = None


class EstudianteResponse(EstudianteBase):
    """
    Schema de respuesta para Estudiante.
    Incluye datos relacionados de Persona.
    """

    id_estudiante: UUID
    persona: PersonaResponse

    class Config:
        from_attributes = True


# ==================== PROFESOR ====================
class ProfesorBase(BaseModel):
    especialidad: str


class ProfesorCreate(PersonaBase, ProfesorBase):
    """
    Schema para crear un profesor (incluye datos de persona).
    """

    usuario_id: Optional[UUID] = None


class ProfesorUpdate(BaseModel):
    """
    Schema para actualizar un profesor (todos los campos opcionales).
    """

    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    especialidad: Optional[str] = None


class ProfesorResponse(ProfesorBase):
    """
    Schema de respuesta de profesor (con datos de persona).
    """

    id_profesor: UUID
    persona: PersonaResponse

    class Config:
        from_attributes = True


# ==================== MATERIA ====================
class MateriaBase(BaseModel):
    """
    Schema base de Materia.
    """

    nombre: str
    codigo: str
    creditos: int
    profesor_id: Optional[UUID] = None


class MateriaCreate(MateriaBase):
    """
    Schema para crear una nueva materia.
    """

    usuario_id: Optional[UUID] = None


class MateriaUpdate(BaseModel):
    """
    Schema para actualizar una materia.
    Todos los campos son opcionales.
    """

    nombre: Optional[str] = None
    codigo: Optional[str] = None
    creditos: Optional[int] = None
    profesor_id: Optional[UUID] = None


class MateriaResponse(MateriaBase):
    """
    Schema de respuesta para una materia.
    Incluye IDs y metadatos.
    """

    id_materia: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== NOTA ====================
class NotaBase(BaseModel):
    """
    Campos base para Nota (comunes entre creación y actualización)
    """
    valor: float
    materia_id: Optional[UUID] = None
    estudiante_id: Optional[UUID] = None
    profesor_id: Optional[UUID] = None


class NotaCreate(BaseModel):
    """
    Schema para la creación de una Nota.
    Requiere estudiante_id, materia_id y valor.
    El profesor puede especificarse manualmente o inferirse.
    """
    estudiante_id: UUID
    materia_id: UUID
    valor: float
    profesor_id: Optional[UUID] = None  # ✅ agregado


class NotaUpdate(BaseModel):
    """
    Schema para actualizar una Nota.
    Todos los campos son opcionales.
    """
    valor: Optional[float] = None
    materia_id: Optional[UUID] = None
    estudiante_id: Optional[UUID] = None
    profesor_id: Optional[UUID] = None


class NotaResponse(BaseModel):
    """
    Respuesta de Nota con relaciones opcionales.
    """
    id_nota: UUID
    valor: float
    fecha_creacion: datetime

    materia_id: Optional[UUID]
    estudiante_id: Optional[UUID]
    profesor_id: Optional[UUID]

    materia_nombre: Optional[str] = None
    estudiante_nombre: Optional[str] = None
    profesor_nombre: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== GRUPO ====================
class GrupoBase(BaseModel):
    """
    Schema base para Grupo.
    """

    nombre: str
    materia_id: UUID
    profesor_id: UUID
    periodo_id: UUID


class GrupoCreate(GrupoBase):
    """
    Schema para creación de Grupo.
    """

    pass


class GrupoUpdate(BaseModel):
    """
    Schema para actualización de Grupo.
    Solo permite cambiar el nombre.
    """

    nombre: Optional[str] = None


class GrupoResponse(GrupoBase):
    """
    Schema de respuesta para Grupo.
    Incluye campos de auditoría.
    """

    id_grupo: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== PERIODO ====================
class PeriodoBase(BaseModel):
    """
    Schema base para Periodo.
    """

    nombre: str
    fecha_inicio: date
    fecha_fin: date


class PeriodoCreate(PeriodoBase):
    """
    Schema para crear un periodo académico.
    """

    pass


class PeriodoUpdate(BaseModel):
    """
    Schema para actualizar un periodo.
    Todos los campos son opcionales.
    """

    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class PeriodoResponse(PeriodoBase):
    """
    Schema de respuesta para un periodo académico.
    Incluye metadatos y relaciones.
    """

    id_periodo: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== AUDITORIA ====================
class AuditoriaResponse(BaseModel):
    id_auditoria: UUID
    usuario_id: UUID
    accion: str
    tabla: str
    fecha: datetime

    class Config:
        from_attributes = True
