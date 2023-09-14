from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id: int
    #title: str
    #content: str
    #published: bool
    created_at : datetime

    class Config:
        orm_mode = True

""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional #----> need | from typing import Optional
    """