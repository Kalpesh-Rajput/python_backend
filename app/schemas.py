from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

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



class PostResponse(PostCreate):
    id : int
    created_at : datetime
    
    class config:
        orm_mode = True
        

class UserCreate(BaseModel):
    email: EmailStr
    password : str
    
class UserOut(BaseModel):
    id    : int
    email : EmailStr
    created_at : datetime
    
    class config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
    