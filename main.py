from typing import Union
from fastapi import FastAPI
from fastapi.params import Body
from schema import Post

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    return {"data":"There will be posts comingsoon"}

@app.post("/posting")
def posting(
    #body:dict = Body(...)): ---> Body extrae el cuerpo del post
    # from fastapi.params import Body ---> nesecita import Body para funcionar
    # es mejor usar pydantic como libreria aparte para extraer y esquematizar los datos requeridos
    new_post:Post
    ):
    print(new_post)
    return {
        # we can format this return
        #'another_think': 'were return',
        #'title':body['title'],
        #'content':body['content'] 
        'another_think': 'were return',
        'title':new_post.title,
        'content':new_post.content
        }