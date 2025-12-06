from pydantic import BaseModel
from typing import List
# article inside userDisplay
class Article(BaseModel):
  title : str
  content : str
  published : bool
  class config():
    orm_mode = True

class UserBase(BaseModel):
  username : str
  email : str
  password : str

class userDisplay(BaseModel):
  username : str
  email : str
  items : List[Article] = []
  class config():
    orm_mode = True

# User inside articleDisplay
class User(BaseModel):
  id: int
  username: str
  class config():
    orm_mode = True

class aricleBase(BaseModel):
  title : str
  content : str
  published : bool
  creator_id : int

class articleDisplay(BaseModel):
  title: str
  content: str
  published: bool
  user: User
  class config():
    orm_mode = True

class ProductBase(BaseModel):
  title: str
  description: str
  price: float