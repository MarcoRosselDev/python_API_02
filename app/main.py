from fastapi import FastAPI
from .routers import post, user
from .database import engine
from . import models
# pip install python-decouple python-dotenv-------------------------------
from decouple import config # to pass env passwords from .env file--------
PASS_DB = config('PASS_DB')
DATABASE_NAME=config('DATABASE_NAME')
#-------------------------------------------------------------------------
import psycopg2
from psycopg2.extras import RealDictCursor

# uvicorn main:app --reload ----------> arrancar un servidor local
# uvicorn app.main:app --reload ------> dentro de una carpeta
models.Base.metadata.create_all(bind=engine)#<-- crea las tablas y columnas de models en la base de datos automaticamente en el momento de arrancar uvicorn
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

# bucle while para que cada 3 segundos trate de conectarse a la base de datos
# motivo: la idea es que nos se puedan ejecutar comandos CRUD mientras no se conecte a la base de datos
# time.sleep() ---> para que espere x segundos para un nuevo intento de coneccion
# motivo2: fallas en la conexion a internet, o la base de dato.
""" while True:
    try:
        # Connect to an existing database
        #conn = psycopg2.connect(host, database, user, password)
        conn = psycopg2.connect(host='localhost', database=DATABASE_NAME, user='postgres', password=PASS_DB, cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cur = conn.cursor() # este cur es importante, con esto operamos CRUD en postgres desde python
        print('successful conection')
        break
    except Exception as error:
        print('no se pudo conectar a la base de datos de postgres')
        print(error)
        time.sleep(4)
"""