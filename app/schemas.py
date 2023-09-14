from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ResponseUserCreated(BaseModel):
    id: int
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional #----> need | from typing import Optional
    """