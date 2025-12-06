from fastapi import APIRouter,Query, Body,Path
from pydantic import BaseModel
from typing import Optional, List, Dict
router = APIRouter(
  prefix='/blog',
  tags=['blog']
)
@router.post('/')
def index():
  return {'message': 'hello world'}
class Image(BaseModel):
  url: str
  alias: str
# Request body (read request body as json)
class blog_model(BaseModel):
  title: str
  content: str
  nb_comments: int   # data validation
  published: Optional[bool]
  tags: List[str] = []
  metadata: Dict[str, str] = {'key1': 'value1'}
  image: Optional[Image] = None

@router.post('/new')
def create_blog(blog: blog_model): # data conversion
  # return "ok" 
  return {'data': blog}  # json schema

# path and query parameters
# combine all 3 types of data
@router.post('/new/{id}')
def create_blog2(blog : blog_model, id: int, version: int = 1):
  return {
    'id': id,
    'data': blog,
    'version': version
    }

# parameter mentadata
# - informarion display in docs
# - using the query, path, and body imports
# - set default values (end at deprecated)
# validators
# - provide a default value
# - require a value (non optional paramenters)(by using elipsis -> ...)
# - min length requirement (content has to be that much big(min), or small(max))
# - regex validation(regular expression)(end)
# multiple values
# - for query parameters (localhost: 8001/blog/new/2/comment?commentId=4&commentID=4&v=1.0&v=1.1&v=1.2&v=3)
# - v: Optional[List[str]] = Query(None)
# - provide default value
# number validators -> for validating numbers
# gt = greater then, ge = greater than or equal to, lt = less than, le = less than or equal to
# complex subtypes
# - pydantic models are not restricted to simple types (check in blog_model class after published)
# - (List, set, dict, tuple)
# cutom model subtype -> (class Image)
@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: blog_model, id: int, comment_title: int = Query(None, title='title of the comment', description='some description of the comment_title', alias='commentTitle', deprecated=True), 
                  # content: str = Body('hi how are you')
                  # content: str = Body(...) # Ellipsis -> can be used in palce of ...
                  content: str = Body(..., min_length=10, max_length=20, regex='^[a-z\s]*$'),
                  # v: Optional[List[str]] = Query(None)
                  v: Optional[List[str]] = Query(['1.0','1.1','1.2']),
                  # comment_id: int = Path(None, gt=5, le=10)
                   ):
  return {'blog': blog,
          'id': id,
          'comment_title': comment_title,
          'content': content,
          'version': v}
          # 'comment_id': comment_id}


# database overview
# 1. dependencies quick intro
# 2. database in FastAPI
# 3. create database and tables
# 4. write data
# 5. create and read
# 6. update and delete
# 7. realtionships

# dependencies
# - allow funcion to depend on another function
# - improt functionality seamlessly
def required_functionality():
  return {'message':'learning fastAPI is important'}
