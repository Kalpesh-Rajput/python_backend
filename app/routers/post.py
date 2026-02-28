from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import schemas,utils,models
from sqlalchemy.orm import Session
from .. database import engine,get_db,SessionLocal
from typing import List
models.Base.metadata.create_all(bind=engine)
from .. import oauth2

router = APIRouter(
    prefix = "/sqlalchemy",
    tags=['Posts']
)
#----------------------------------------------------------------------------------------------------------------
## SQLALchemy

# @app.get("/sqlalchemy")
# def test_post(db : Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     # print(post)
#     return {"data" : post}


# to Get the post from SQ db
@router.get("/")
def get_post(db : Session = Depends(get_db) , get_current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).all()
    return  post


# Creating post and storing all the post in SQL DB
@router.post("/" , status_code=status.HTTP_201_CREATED , )
def create_posts(post:schemas.PostCreate,db : Session = Depends(get_db) , get_current_user : int = Depends(oauth2.get_current_user)) :
    print(post.dict())
    new_post = models.Post(title = post.title , content = post.content,published = post.published)
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/{id}")
def get_post(id : int , db : Session = Depends(get_db), get_current_user : int = Depends(oauth2.get_current_user)):
    fetch_post =db.query(models.Post).filter(models.Post.id == id).first()
    print(fetch_post)
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    return fetch_post


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int , db : Session = Depends(get_db), get_current_user : int = Depends(oauth2.get_current_user)):
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
    
    
@router.put("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def update_post(id : int , post_data : schemas.PostCreate, db : Session = Depends(get_db), get_current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    
    
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f"post with id : {id} does not exist")
    post_query.update(post_data.dict(),synchronize_session = False)
    
    db.commit()
    return db_post 