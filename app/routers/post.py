from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from .. import schemas,utils,models
from sqlalchemy.orm import Session
from .. database import engine,get_db,SessionLocal
from typing import List,Optional
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
@router.get("/" , response_model=List[schemas.PostResponse])
def get_post(db : Session = Depends(get_db) , 
             current_user : int = Depends(oauth2.get_current_user),
             limit : int = 10, skip : int = 0,search : Optional[str] = ""):
    # post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() this is for getting the post of the current user only
    # posts = db.query(models.Post).all() # this is for getting all the post of all the users
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # limit will limit the posts &Skip will skip the first 2 post and then return the rest of the post
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} does not exist")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorised to perform requested action")
    
    return posts
    




# Creating post and storing all the post in SQL DB
@router.post("/" , status_code=status.HTTP_201_CREATED ,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db : Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)) :
    
    print(current_user.id)
    # new_post = models.Post(**post.dict())
    new_post = models.Post(
        owner_id=current_user.id,   # ✅ ADD THIS
        **post.dict()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    
    # print(post.dict())
    # new_post = models.Post(title = post.title , content = post.content,published = post.published)
    # # new_post = models.Post(**post.dict())
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    # return  new_post

@router.get("/{id}")
def get_post(id : int , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    posts =db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorised to perform requested action")
    

    return posts


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int , db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #                DELETE FROM posts WHERE id = %s RETURNING *
    #                """ , (str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def update_post(id : int , post_data : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f"post with id : {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorised to perform requested action")
    
    post_query.update(post_data.dict(),synchronize_session = False)
    
    db.commit()
    return post 