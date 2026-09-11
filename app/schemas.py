from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

class DireccionBase(BaseModel):
    calle_numero: str
    distrito: str
    referencia: Optional[str] = None

class DireccionCreate(DireccionBase):
    pass

class DireccionResponse(DireccionBase):
    id_direccion: int
    id_usuario: int

    class Config:
        from_attributes = True

class UserSignup(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    password: str
    fecha_nacimiento: date

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    email: str
    fecha_nacimiento: date
    fecha_registro: datetime
    direcciones: List[DireccionResponse] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse