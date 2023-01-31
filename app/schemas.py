import email
from secrets import token_bytes
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional



#---------------------USER--------------------------------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

#-------------------------------POST--------------------
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):  
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # votes: int
    class Config:  #this sets the sqlalchemy model to be recongnised by pydantic model
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:  #this sets the sqlalchemy model to be recongnised by pydantic model
        orm_mode = True

#--------------------LOGIN----------------------------------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None

#-------------Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore