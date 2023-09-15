from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Response
from .. import models, oauth2, schemas

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )

@router.get("/", 
    response_model=List[schemas.PostBase] # cuando retornamos una lista requerimos List from typing
    # para que formatee la respuesta en una lista
    )
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

""" @router.post("/", 
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.PostCreate)  # esquema de retorna, para omitir info al retornar
def posting(
    post:schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
    ):
    #-------------------------------- codigo previo (sql lenguage) -----------------------------------------------------------
    # cur.execute'''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (post.title, post.content, post.published))
    #posts_db = cur.fetchone()
    #conn.commit()
    #--------------------------------------------------------------------------------------------------------------------------
    #----------->posts_db = models.Post(title=post.title, content=post.content)
    print(current_user)
    posts_db = models.Post(**post.dict())
    # en caso de que el modelo sea muy largo podemos convertir post(parametro) en diccionario y pasarlo a models.Post
    # post_db = models.Post(**post.dict())
    # por ahora lo dejos asi por que es mas visual y entendible para mi
    db.add(posts_db) # agregar la peticion a la seccion local db
    db.commit() # para guardar los cambios, si no no se salvan los cambios
    db.refresh(posts_db) # refresca para que podamos ver el retorno, si no retorna {} vacio
    return posts_db # ojo, error si retornamos {'data': posts_db}
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}",
    response_model=schemas.PostCreate
    )
def get_one(
    id:int,
    db: Session = Depends(get_db)
    ):
    # algun mecanismo para encontrar el id en la base de datos
    # si no esta prosesamos el status = 404
    #cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #found_post = cur.fetchone()
    post_id = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_id:
        # we need | from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'no se encontro el id {id}')
        # queda mas ordenado en una sola linea con HTTPException
    return post_id

@router.delete("/{id}", 
    status_code=status.HTTP_403_FORBIDDEN
    )
def delete_post(
    id:int,
    db: Session = Depends(get_db)
    ):
    found_post_to_delete = db.query(models.Post).filter(models.Post.id == id)
    first_one = found_post_to_delete.first()

    if first_one == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id :{id} doesn not exist')
    
    found_post_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",
    response_model=schemas.PostCreate)
def update_post(
    id:int, 
    post:schemas.PostCreate,
    db: Session = Depends(get_db)
    ):
    #cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # vamos a probar sqlalchemy:
    # es una libreria no relacionada con FastAPI que realiza consultas sql en codigo python
    #updated_post = cur.fetchone()
    #conn.commit()
    found_post_update = db.query(models.Post).filter(models.Post.id == id)
    first_one = found_post_update.first()
    if not first_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    found_post_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return found_post_update.first()
