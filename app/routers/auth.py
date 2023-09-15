from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login_user(
    user_credentials:OAuth2PasswordRequestForm = Depends(),
    db: Session=Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    # si paso los dos if, crear un token y retornarlo
    access_token = create_access_token(data={"user_id":user.id})# data=lo que queramos enviar en payload data
    return {"access token":access_token,
            "token_type": "bearer"}