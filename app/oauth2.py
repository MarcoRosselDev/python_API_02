from jose import JWSError, jwt
from datetime import datetime, timedelta
#-------------env
from decouple import config
SECRET_KEY = config('SECRET_KEY_JOSE_LB')
ALGORITHM=config('ALGORITHM')
EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=int(EXPIRE_MINUTES))
    to_encode.update({'exp': expire})#<---- como ya es un dict le agregamos otra llave,valor={}
    encoded_jWt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jWt