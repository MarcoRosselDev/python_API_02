""" from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
#-------------
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
#-------------env
from decouple import config
#SECRET_KEY = config('SECRET_KEY_JOSE_LB')
SECRET_KEY = "alkjsdf12349124asdfa2346sdfgsdft343434gtsdfgdf324964385sdfgs"
#ALGORITHM=config('ALGORITHM')
ALGORITHM= 'HS256'
#EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES')
EXPIRE_MINUTES= 300

#barrera fastapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({'exp': expire})#<---- como ya es un dict le agregamos otra llave,valor={}
    encoded_jWt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jWt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception) """

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
#from .config import settings
from decouple import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = config('SECRET_KEY_JOSE_LB')
ALGORITHM=config('ALGORITHM')
EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
#
    token = verify_access_token(token, credentials_exception)#

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user