from typing import Optional,List
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI, Response,status,HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import random
from app import schemas,utils,models
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from app.database import engine,get_db
import time




app  = FastAPI()

   
try:
    conn = psycopg2.connect(host = 'localhost',database = 'postgres',user = 'postgres',password = '740542',cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("database connection was succesful.....!")

except Exception as error:
    print("Connection to databasse failed")
    print("Error : " , error)
    


    
    
# we add below in to Schemas.py
    

class Post(BaseModel):
    title : str
    content : str
    published : bool  = True 
    # rating : Optional[int] = None  # comment this just for sql alchemy has gettign error for rating

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

@app.get("/")
def root():
    return {"message" : "testing"}


@app.get("/post")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return  posts

# same as above code
# @app.get("/post")
# def get_post():
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM posts")
#         posts = cursor.fetchall()
#         return {"data": posts}
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()

#---------------------------------------------------------------------------------------------------

# # storing all the post in to dict
# @app.post("/post" , status_code=status.HTTP_201_CREATED )# if we dont mentioned it so will get status code 200 OK bu this is wrong we need 201 CREATED
# def create_post(post : Post):
#     post_dict = post.dict()
#     post_dict['id'] =random.randrange(0,1000000)
#     my_post.append(post_dict)
#     return {"data" : post_dict}

# Creating post and storing all the post in SQL DB
@app.post("/post" , status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: Post) :
    cursor.execute("""
                   INSERT INTO posts(title,content,published) VALUES (%s,%s,%s)
                    RETURNING *
                   """,(post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    return new_post
    
# @app.post("/post", status_code=status.HTTP_201_CREATED)   # storing data in to db
# def create_post(post: Post):
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#             INSERT INTO posts (title, content, published, rating)
#             VALUES (%s, %s, %s, %s)
#             RETURNING *
#             """,
#             (post.title, post.content, post.published, post.rating)
#         )
#         new_post = cursor.fetchone()
#         conn.commit()
#         return {"data": new_post}
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()




# -------------------------------------------------------------------------------------------------
# for both of the below order matter cause if we keep {id route first then we will get error}
@app.get("/post/latest")
def get_latest_post():
    post = my_post[len(my_post) -1]
    return post


# @app.get("/post/{id}")
# def get_post(id : int, response : Response):
#     # print(type(id))
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND  # WE CAN DO THIS BY USING HTTPEXCEPTION
#         # return {"message" : f"post with id :{id} was not found"}
#     # print(post)
#     return {"post detail" : post}


# With SQL

@app.get("/post/{id}")
def get_post(id : int , response : Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """ , (str(id)))
    test_post = cursor.fetchone()
    # print(test_post)
    return test_post

# -------------------------------------------------------------------------------------------------

# deleting post with help of (find index post function)
 
# @app.delete("/post/{id}" , status_code=status.HTTP_204_NO_CONTENT)
# def delet_post(id:int):
#     # deleting post
#     # find the index in array that has required id
#     # my_post.pop(index)
#     index = find_index_post(id)
    
#     if index == None:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} does not exist")
#     my_post.pop(index)
#     # return {"message" : f"post was succesfully deleted of id : {id}"} 
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# deleting post in SQL DB
@app.delete("/post/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id:int):
    cursor.execute("""
                   DELETE FROM posts WHERE id = %s RETURNING *
                   """ , (str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} does not exist")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# -----------------------------------------------------------------------------------------------------------------
# Updating Post
# @app.put("/post/{id}")
# def update_post(id : int , post : Post):
#     index = find_index_post(id)
    
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
#                             detail=f"post with id : {id} does not exist")
        
#     post_dict = post.dict()
#     post_dict['id'] = id 
#     my_post[index] = post_dict 
#     return {"data" : post_dict} # "originalData" : my_post we can also return this original content 

# Updating post in SQL DB
@app.put("/post/{id}")
def update_post(id : int , post : Post):
    cursor.execute("""
                   UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *  
                   """ , (post.title , post.content , post.published , str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f"post with id : {id} does not exist")
    return updated_post 


#----------------------------------------------------------------------------------------------------------------
## SQLALchemy

from . import models
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

# @app.get("/sqlalchemy")
# def test_post(db : Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     # print(post)
#     return {"data" : post}


# to Get the post from SQ db
@app.get("/sqlalchemy")
def get_post(db : Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return  post


# Creating post and storing all the post in SQL DB
@app.post("/sqlalchemy" , status_code=status.HTTP_201_CREATED )
def create_posts(post:schemas.PostCreate,db : Session = Depends(get_db)) :
    print(post.dict())
    new_post = models.Post(title = post.title , content = post.content,published = post.published)
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@app.get("/sqlalchemy/{id}")
def get_post(id : int , db : Session = Depends(get_db)):
    fetch_post =db.query(models.Post).filter(models.Post.id == id).first()
    print(fetch_post)
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    return fetch_post


@app.delete("/sqlalchemy/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int , db : Session = Depends(get_db)):
    # cursor.execute("""
    #                DELETE FROM posts WHERE id = %s RETURNING *
    #                """ , (str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} does not exist")
    post_query.delete(synchronize_session = False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/sqlalchemy/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def update_post(id : int , post_data : schemas.PostCreate, db : Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    
    
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f"post with id : {id} does not exist")
    post_query.update(post_data.dict(),synchronize_session = False)
    
    db.commit()
    return db_post 


# ------------------------------------------------------------------------------------------------------------------------
# Register Users

@app.post("/users" , status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate,db : Session = Depends(get_db)):
    
    # Hash the password
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


# Get Users
@app.get("/users/{id}" , response_model=schemas.UserOut)
def get_user(id : int , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} does not exist")
    return user
