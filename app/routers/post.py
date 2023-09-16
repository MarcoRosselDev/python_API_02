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
    response_model=List[schemas.Post] # cuando retornamos una lista requerimos List from typing
    # para que formatee la respuesta en una lista
    )
def get_posts(
    db: Session = Depends(get_db), #--> abre y cierra una session en data base de postgres
    user_id: int=Depends(oauth2.get_current_user) #--> desencripta la llave foranea para obtener info del usuario y su key
    ):
    posts = db.query(models.Post).filter(models.Post.owner_id == user_id.id).all()
    return posts

@router.post("/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.Post
    )
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db), 
    user_id: int=Depends(oauth2.get_current_user)
    ):
    #print(user_id, 'print id')
    new_post = models.Post(owner_id=user_id.id, # --> owner_id de schema le damos el valor de la llave foranea decodificada.
        **post.dict() # --> lo demas lo extraemos del schema post. convertido en dictionari.
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}",
    response_model=schemas.Post
    )
def get_one(
    id:int,
    db: Session = Depends(get_db),
    user_id: int=Depends(oauth2.get_current_user)
    ):
    # algun mecanismo para encontrar el id en la base de datos
    # si no esta prosesamos el status = 404
    #cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #found_post = cur.fetchone()
    print(user_id.email, "email user")
    print(user_id.id, "id user")
    post_id = db.query(models.Post).filter(models.Post.id == id).first()
    first_one = post_id
    if not post_id:
        # we need | from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'no se encontro el id {id}')
    if post_id.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You're not authorized to see this post")
        # queda mas ordenado en una sola linea con HTTPException
    return post_id

@router.delete("/{id}", 
    status_code=status.HTTP_403_FORBIDDEN
    )
def delete_post(
    id:int,
    db: Session = Depends(get_db),
    user_id: int=Depends(oauth2.get_current_user)
    ):
    found_post_to_delete = db.query(models.Post).filter(models.Post.id == id)
    first_one = found_post_to_delete.first()

    if first_one == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id :{id} doesn not exist')
    print(user_id.id, 'user id')
    print(type(user_id.id))
    print(first_one.owner_id)
    if first_one.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action')
    found_post_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",
    response_model=schemas.Post)
def update_post(
    id:int, 
    post:schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int=Depends(oauth2.get_current_user)
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
    if first_one.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action')
    found_post_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return found_post_update.first()
