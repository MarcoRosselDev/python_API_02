from fastapi import FastAPI, status, HTTPException
from .schema import Post
# pip install python-decouple python-dotenv-------------------------------
from decouple import config # to pass env passwords from .env file--------
PASS_DB = config('PASS_DB')
DATABASE_NAME=config('DATABASE_NAME')
#-------------------------------------------------------------------------
import psycopg2
from psycopg2.extras import RealDictCursor

# uvicorn main:app --reload ----------> arrancar un servidor local
# uvicorn app.main:app --reload ------> dentro de una carpeta
app = FastAPI()

# bucle while para que cada 3 segundos trate de conectarse a la base de datos
# motivo: la idea es que nos se puedan ejecutar comandos CRUD mientras no se conecte a la base de datos
import time # time.sleep() ---> para que espere x segundos para un nuevo intento de coneccion
# motivo2: fallas en la conexion a internet, o la base de dato.
while True:
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

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return{'data':posts}

@app.post("/posts",
        status_code=status.HTTP_201_CREATED # por ahora, por que regresava 200 = ok
        )
def posting(
    #body:dict = Body(...)): ---> Body extrae el cuerpo del post
    # from fastapi.params import Body ---> nesecita import Body para funcionar
    # es mejor usar pydantic como libreria aparte para extraer y esquematizar los datos requeridos
    post:Post
    ):
    cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    posts_db = cur.fetchone()
    conn.commit()
    return {
        'data': posts_db
        }

@app.get("/posts/{id}")
def get_one(id:int):
    # algun mecanismo para encontrar el id en la base de datos
    # si no esta prosesamos el status = 404
    cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    found_post = cur.fetchone()
    if not found_post:
        # we need | from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no se encontro el id {id}')
        # queda mas ordenado en una sola linea con HTTPException
    return {"id was": found_post}

@app.delete("/posts/{id}", status_code=status.HTTP_403_FORBIDDEN)
def delete_post(id:int):
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    found_delete = cur.fetchone()

    if not found_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'post deleted': found_delete}