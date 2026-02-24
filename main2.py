from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, ConfigDict
from typing import Optional

app = FastAPI()



# http://127.0.0.1:8000/?type=yolo we should run this 
# @app.get("/")
# async def root(type:str = "normal"):
#     if type == "yolo":
#         return {"yolo":"You only live once"}
#     return {"message": "Chal nikal"}


class Post(BaseModel):
    title: str
    content : str
    published : bool = True
    rating : Optional[int] = None 

@app.get("/")
async def root():
    print("Chal hettt")
    return {"message": "Chal nikal"}


# @app.post("/post")
# async def soot(load : dict = Body(...)):
#     print(load)
#     return {"New post": f"title: {load['title']} content: {load['contennt']}"}

@app.post("/createposts")
def create_post(new_post : Post):
    print(new_post)
    print(new_post.dict())
    return {
        "status": "success",
        "data": new_post
    }
    




