from fastapi import APIRouter, status, Response, Depends
from router.blog_post import required_functionality
from enum import Enum
from typing import Optional
router = APIRouter(
  prefix='/blog',
  tags=['blog']
)
# @router.post('/post')
# def practice2():
#   return 'hi'
# @router.get('/hello')
# def practice3():
#   return {'message': 'hello world'}
# @app.get('/blog/all')
# def get_all_blogs():
#   return {'message': 'All blogs provided'}
# @app.get('/blog/all')
# def get_all_blogs(page=1, page_size=10):
#   return {'message': f'all {page_size} blog on {page}'}
@router.get('/all', summary='retrieve all bolgs', description='this api call stimulates fetching all blogs', response_description='list of available blogs')
def get_all_blogs(page=1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)):
  return {'message': f'all {page_size} blog on {page}', 'req': req_parameter}
@router.get('/{id}/comments/{comments_id}', tags=[ 'comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
  """
  stimulates retriveing a comment of a blog

  - **id** mandatory path parameter
  - **comment_id** mandatory path parameter
  - **valid** optional query parameter
  - **username** optional query parameter
  """
  return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}
class blog_type(str, Enum):
  short = 'short'
  story = 'story'
  howto = 'howto'
@router.get('/type/{type}') 
def get_blog_type(type: blog_type):
  return {'message': f'blog of type {type}'}
# @app.get('/blog/{id}, status_code = 404')
# def get_blog(id: int):
#   if id > 5:
#     return {'error': f'Blog {id} not found'}
#   else:
#     return {'message': f'Blog with id {id}'}
@router.get('/{id}', status_code = status.HTTP_200_OK, tags=['blog'])
def get_blog(id: int, response: Response):
  if id > 5:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'error': f'Blog {id} not found'}
  else:
    response.status_code = status.HTTP_200_OK
    return {'message': f'Blog with id {id}'}
# code below give error while serching on server cause of parameter type selected in first blog
# however if the code is putted before that selected parameter type blog then all will run correctly
# @app.get('/blog/all')
# def get_all_blogs():
#   return {'message': 'All blogs provided'}