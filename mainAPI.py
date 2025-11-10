"""
Sistema de Gestión Escolar
API REST con FastAPI, SQLAlchemy y PostgreSQL (Neon)
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
from apis import (
    auditoria,
    estudiante,
    grupo,
    materia,
    nota,
    periodo,
    persona,
    profesor,
    usuario,
)

# Base de datos
from database.config import create_tables


app = FastAPI(
    title="Sistema de Gestión Escolar",
    description=(
        "API REST para la gestión de usuarios, profesores, estudiantes, "
        "materias, grupos, periodos, notas y auditorías en una institución educativa."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # 👈 URL de tu frontend Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auditoria.router, prefix="/auditorias", tags=["Auditoría"])
app.include_router(estudiante.router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(grupo.router, prefix="/grupos", tags=["Grupos"])
app.include_router(materia.router, prefix="/materias", tags=["Materias"])
app.include_router(nota.router, prefix="/notas", tags=["Notas"])
app.include_router(periodo.router, prefix="/periodos", tags=["Periodos"])
app.include_router(persona.router, prefix="/personas", tags=["Personas"])
app.include_router(profesor.router, prefix="/profesores", tags=["Profesores"])
app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación."""
    print("Iniciando Sistema de Gestión Escolar...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")

@app.get("/", tags=["Raíz"])
async def root():
    """Información general de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión Escolar",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "usuarios": "/usuarios",
            "profesores": "/profesores",
            "estudiantes": "/estudiantes",
            "materias": "/materias",
            "grupos": "/grupos",
            "notas": "/notas",
            "periodos": "/periodos",
            "personas": "/personas",
            "auditorias": "/auditorias",
        },
    }

def main():
    """Función principal para ejecutar el servidor FastAPI."""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "mainAPI:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

if __name__ == "__main__":
    main()
