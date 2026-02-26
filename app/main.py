from typing import Optional,List
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
import random
from . import schemas,utils,models
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . database import engine,get_db
import time
from .routers import post,user




app  = FastAPI()

   
try:
    conn = psycopg2.connect(host = 'localhost',database = 'postgres',user = 'postgres',password = '740542',cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("database connection was succesful.....!")

except Exception as error:
    print("Connection to databasse failed")
    print("Error : " , error)
    


my_post = [
           {"title" : "fav food" , "content" : "pizza" , "id" : 2},
           {"title" : "title of the post 1" , "content" : "content of the post 1" , "id" : 1}
           ]


def find_post(id):
    for p in my_post:
        if p["id"] == int(id):
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)



@app.get("/")
def root():
    return {"message" : "testing"}


