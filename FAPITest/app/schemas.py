from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional

"""
User = [ 
    id, email, created_at,      default
    account_id, account,        expandable obj
]

Account = [
    id, dob                     default
]

Post =[
    id, created_at,             default
    title, content              default
    owner_id,owner              expandable obj
    votes,                      expandable list
]

Vote =[
    user_id            expandable obj
]

"""

class Account(BaseModel):
    id :str
    dob: datetime

    class Config:
        orm_mode=True

class User(BaseModel):
    id : str
    email: EmailStr
    created_at: datetime

    account_id: Optional[str]
    account: Optional[Account] 

    class Config:
        orm_mode=True

class Vote(BaseModel):
    user_id: Optional[str]
    user: Optional[User]

    class Config:
        orm_mode=True

class Post(BaseModel):
    id : str
    created_at: str
    title: str
    content: str

    user_id: Optional[str]
    user: Optional[User]

    total_votes : int

    votes : Optional[list[Vote]]

    class Config:
        orm_mode=True

##################################
###########Temp Schemas###########
##################################

# for Post
class TempPost(BaseModel):
    data : Post = ""
    error : str = ""


##################################
##################################



class PostBase(BaseModel):
    title : str
    content : str

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode=True

class PostIn(PostBase):
    id : int 
    created_at : datetime
    user_id : int
    owner : UserOut
    class Config:
        orm_mode = True
class PostOut(BaseModel):
    Post : Post
    votes : int 
    class Config():
        orm_mode=True

class UserIn(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type:str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None

class VoteIn(BaseModel):
    post_id : int
    direction : conint(le=1)
