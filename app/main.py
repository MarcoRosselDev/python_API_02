from fastapi import FastAPI, status, HTTPException, Depends
from .schemas import Post
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
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

# bucle while para que cada 3 segundos trate de conectarse a la base de datos
# motivo: la idea es que nos se puedan ejecutar comandos CRUD mientras no se conecte a la base de datos
import time # time.sleep() ---> para que espere x segundos para un nuevo intento de coneccion
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
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"data": posts}

@app.post("/posts",
        status_code=status.HTTP_201_CREATED # por ahora, por que regresava 200 = ok
        )
def posting(
    #body:dict = Body(...)): ---> Body extrae el cuerpo del post
    # from fastapi.params import Body ---> nesecita import Body para funcionar
    # es mejor usar pydantic como libreria aparte para extraer y esquematizar los datos requeridos
    post:Post,
    db: Session = Depends(get_db)
    ):
    #-------------------------------- codigo previo (sql lenguage) -----------------------------------------------------------
    # cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #posts_db = cur.fetchone()
    #conn.commit()
    #--------------------------------------------------------------------------------------------------------------------------
    posts_db = models.Post(title=post.title, content=post.content)
    # en caso de que el modelo sea muy largo podemos convertir post(parametro) en diccionario y pasarlo a models.Post
    # post_db = models.Post(**post.dict())
    # por ahora lo dejos asi por que es mas visual y entendible para mi
    db.add(posts_db) # agregar la peticion a la seccion local db
    db.commit() # para guardar los cambios, si no no se salvan los cambios
    db.refresh(posts_db) # refresca para que podamos ver el retorno, si no retorna {} vacio
    return {'data': posts_db}

@app.get("/posts/{id}")
def get_one(
    id:int,
    db: Session = Depends(get_db)
    ):
    # algun mecanismo para encontrar el id en la base de datos
    # si no esta prosesamos el status = 404
    #cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #found_post = cur.fetchone()
    post_id = db.query(models.Post).filter(models.Post.id == id).first( )
    if not post_id:
        # we need | from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no se encontro el id {id}')
        # queda mas ordenado en una sola linea con HTTPException
    return {"id was": post_id}


@app.delete("/posts/{id}", status_code=status.HTTP_403_FORBIDDEN)
def delete_post(
    id:int,
    db: Session = Depends(get_db)
    ):
    #cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #found_delete = cur.fetchone()
    #conn.commit()
    found_post_to_delete = db.query(models.Post).filter(models.Post.id == id)

    if not found_post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    found_post_to_delete.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

'''
@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # vamos a probar sqlalchemy:
    # es una libreria no relacionada con FastAPI que realiza consultas sql en codigo python
    updated_post = cur.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    return {'post deleted': updated_post}
'''