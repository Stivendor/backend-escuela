from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud.usuario_crud import autenticar_usuario
from models.auth import LoginRequest
from utils.auth_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    usuario = autenticar_usuario(db, request.username, request.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = create_access_token({"sub": usuario.username})

    return {
        "token": token,
        "userId": usuario.id_usuario,
        "role": usuario.rol
    }
