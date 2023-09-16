from fastapi import FastAPI
from .routers import post, user, auth
from .database import engine
from . import models

# uvicorn main:app --reload ----------> arrancar un servidor local
# uvicorn app.main:app --reload ------> dentro de una carpeta
models.Base.metadata.create_all(bind=engine)#<-- crea las tablas y columnas de models en la base de datos automaticamente en el momento de arrancar uvicorn
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# just for referens
# pip install python-decouple python-dotenv-------------------------------
#from decouple import config # to pass env passwords from .env file--------
#PASS_DB = config('PASS_DB')
#DATABASE_NAME=config('DATABASE_NAME')
#-------------------------------------------------------------------------