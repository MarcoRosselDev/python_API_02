from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel

class Item(BaseModel):
    title: str
    content: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    return {"data":"There will be posts comingsoon"}

@app.post("/posting")
def posting(body:dict = Body(...)):
    print(body)
    return {'post':body}