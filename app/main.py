from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.models import Usuario, Direccion
from app import schemas, auth

# Crea las tablas si no existen al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CloudEats - Customer Microservice",
    description="API REST de Gestión de Usuarios y Autenticación",
    version="1.0.0"
)

# --- AUTENTICACIÓN ---

@app.post("/api/v1/auth/signup", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    hashed_pwd = auth.get_password_hash(user_data.password)
    new_user = Usuario(
        nombres=user_data.nombres,
        apellidos=user_data.apellidos,
        email=user_data.email,
        password_hash=hashed_pwd,
        fecha_nacimiento=user_data.fecha_nacimiento
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = auth.create_access_token(data={"sub": str(new_user.id_usuario)})
    return {"access_token": access_token, "token_type": "bearer", "user": new_user}


@app.post("/api/v1/auth/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    access_token = auth.create_access_token(data={"sub": str(user.id_usuario)})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# --- PERFIL Y DIRECCIONES ---

@app.get("/api/v1/users/me", response_model=schemas.UserResponse)
def get_my_profile(current_user: Usuario = Depends(auth.get_current_user)):
    return current_user


@app.get("/api/v1/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.post("/api/v1/users/me/direcciones", response_model=schemas.DireccionResponse, status_code=status.HTTP_201_CREATED)
def create_direccion(
    direccion: schemas.DireccionCreate,
    current_user: Usuario = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    new_dir = Direccion(
        id_usuario=current_user.id_usuario,
        calle_numero=direccion.calle_numero,
        distrito=direccion.distrito,
        referencia=direccion.referencia
    )
    db.add(new_dir)
    db.commit()
    db.refresh(new_dir)
    return new_dir