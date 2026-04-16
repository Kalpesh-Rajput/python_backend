from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title : str
    content : str
    published : bool  = True 
    # rating : Optional[int] = None  # comment this just for sql alchemy has gettign error for rating
    
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostDelete(PostBase):
    pass 


    
class UserOut(BaseModel):
    id    : int
    email : EmailStr
    created_at : datetime
    
    model_config = {
    "from_attributes": True
}
    # class Config:
    #     orm_mode = True
 

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    # class Config:
    #     orm_mode = True
        
    model_config = {
    "from_attributes": True
}
   



class PostResponse(PostCreate):
    id : int
    created_at : datetime
    owner_id : int
    
    model_config = {
    "from_attributes": True
}
    
    # class Config:
    #     orm_mode = True
        

class UserCreate(BaseModel):
    email: EmailStr
    password : str
    
        
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None

class vote(BaseModel):
    post_id : int
    dir : conint(le=1) # this means that the value of dir can only be 0 or 1

    