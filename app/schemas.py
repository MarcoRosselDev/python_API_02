from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


""" class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True """

class Post(PostBase):
    id: int
    #created_at: datetime
    owner_id: int


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    #id: str | None = None
    id_user: str

""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional #----> need | from typing import Optional
    """