from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas
#-------------
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
#-------------env
from decouple import config
SECRET_KEY = config('SECRET_KEY_JOSE_LB')
ALGORITHM=config('ALGORITHM')
EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES')

#barrera fastapi
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(EXPIRE_MINUTES))
    to_encode.update({'exp': expire})#<---- como ya es un dict le agregamos otra llave,valor={}
    encoded_jWt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jWt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user:str = payload.get("user_id")
        if id_user is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id_user)
    except JWSError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)