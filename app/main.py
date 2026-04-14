from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth
from .config import settings

print(settings.path)




models.Base.metadata.create_all(bind=engine)


app  = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message" : "testing"}


# my_post = [
#            {"title" : "fav food" , "content" : "pizza" , "id" : 2},
#            {"title" : "title of the post 1" , "content" : "content of the post 1" , "id" : 1}
#            ]


# def find_post(id):
#     for p in my_post:
#         if p["id"] == int(id):
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p['id'] == id:
#             return i



