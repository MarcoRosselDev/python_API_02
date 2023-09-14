from ..schemas import ResponseUserCreated, UserCreate
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import hash_pwd
from fastapi import APIRouter, status, HTTPException, Depends
from .. import models

router = APIRouter()

@router.post("/users", 
        response_model=ResponseUserCreated,
        status_code=status.HTTP_201_CREATED)
def create_user(
    user:UserCreate,
    db: Session = Depends(get_db)
    ):
    pwd = hash_pwd(user.password)
    user.password = pwd
    user_db = models.User(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@router.get("/users/{id}", response_model=ResponseUserCreated)
def found_user(
    id:int,
    db: Session = Depends(get_db)
    ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with id: {id} was not founded')
    return user