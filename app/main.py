from fastapi import FastAPI, status, HTTPException
from .schema import Post

# uvicorn main:app --reload ----------> arrancar un servidor local
# uvicorn app.main:app --reload ------> dentro de una carpeta 
app = FastAPI()

@app.post("/posts", 
        status_code=status.HTTP_201_CREATED # por ahora, por que regresava 200 = ok
        )
def posting(
    #body:dict = Body(...)): ---> Body extrae el cuerpo del post
    # from fastapi.params import Body ---> nesecita import Body para funcionar
    # es mejor usar pydantic como libreria aparte para extraer y esquematizar los datos requeridos
    new_post:Post
    ):
    return {
        # we can format this return
        #'another_think': 'were return',
        #'title':body['title'],
        #'content':body['content'] 
        'another_think': 'were return',
        'title':new_post.title,
        'content':new_post.content
        }

@app.get("/posts/{id}")
def get_one(id:int):
    # algun mecanismo para encontrar el id en la base de datos
    # si no esta prosesamos el status =
    found_post = False
    if not found_post:
        # we need | from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no se encontro el id {id}')
        # queda mas ordenado en una sola linea con HTTPException
    return {"id was": id}