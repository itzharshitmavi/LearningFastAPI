from anyio import TypedAttributeLookupError
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from exceptions import storyException
from router import article, blog_get, blog_post, products, user,files, dependencies
from auth import authentication
from db import models
from db.database import engine
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(files.router)
app.include_router(templates.router)
app.include_router(products.router)
app.include_router(dependencies.router)
@app.get('/hello')
def practice():
  return 'Hello world'
@app.exception_handler(storyException)
def story_exception_handler(request: Request, exc: storyException):
  return JSONResponse(status_code=418, content={'details': exc.name})
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: storyException):
#   return PlainTextResponse(str(exc), status_code=400)

@app.get("/")
async def get():
  return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  clients.append(websocket)
  while True:
    data = await websocket.receive_text()
    for client in clients:
      await client.send_text(data)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  duration = time.time() - start_time
  response.headers['duration'] = str(duration)
  return response

origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["+"],
  allow_headers = ["+"]
)
# to show image in browser
app.mount('/files', StaticFiles(directory='files'), name = 'files')
app.mount('/templates/static', StaticFiles(directory="templates/static"), name="static")

# parameters overview
# 1. request body
# 2. path and query parameters
# 3. parameter metadata
# 4. validators
# 5. multiple values
# 6. number validators
# 7. complex subtype

# some other important concepts
# - error handling
# -- HTTP Status Codes
# --- 1xx -> informational
# --- 2xx -> success
# --- 3xx -> redirection
# --- 4xx -> client error
# --- 5xx -> server error
# - custom responses -> standard response is a model, list, database model, dict etc, we can customize the response object, No data conversion
# - headers
# - cookies
# - form data
# - CORS (Cross Origin Resource Sharing)
#

# @app.post('/post')
# def practice2():
#   return 'hi'
# @app.get('/hello')
# def practice3():
#   return {'message': 'hello world'}
# # @app.get('/blog/all')
# # def get_all_blogs():
# #   return {'message': 'All blogs provided'}
# # @app.get('/blog/all')
# # def get_all_blogs(page=1, page_size=10):
# #   return {'message': f'all {page_size} blog on {page}'}
# @app.get('/blog/all', tags=['blog'], summary='retrieve all bolgs', description='this api call stimulates fetching all blogs', response_description='list of available blogs')
# def get_all_blogs(page=1, page_size: Optional[int] = None):
#   return {'message': f'all {page_size} blog on {page}'}
# @app.get('blog/{id}/comments/{comments_id}', tags=['blog', 'comment'])
# def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
#   """
#   stimulates retriveing a comment of a blog

#   - **id** mandatory path parameter
#   - **comment_id** mandatory path parameter
#   - **valid** optional query parameter
#   - **username** optional query parameter
#   """
#   return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}
# class blog_type(str, Enum):
#   short = 'short'
#   story = 'story'
#   howto = 'howto'
# @app.get('/blog/type/{type}', tags=['blog']) 
# def get_blog_type(type: blog_type):
#   return {'message': f'blog of type {type}'}
# # @app.get('/blog/{id}, status_code = 404')
# # def get_blog(id: int):
# #   if id > 5:
# #     return {'error': f'Blog {id} not found'}
# #   else:
# #     return {'message': f'Blog with id {id}'}
# @app.get('/blog/{id}', status_code = status.HTTP_200_OK, tags=['blog'])
# def get_blog(id: int, response: Response):
#   if id > 5:
#     response.status_code = status.HTTP_404_NOT_FOUND
#     return {'error': f'Blog {id} not found'}
#   else:
#     response.status_code = status.HTTP_200_OK
#     return {'message': f'Blog with id {id}'}
# # code below give error while serching on server cause of parameter type selected in first blog
# # however if the code is putted before that selected parameter type blog then all will run correctly
# # @app.get('/blog/all')
# # def get_all_blogs():
# #   return {'message': 'All blogs provided'}