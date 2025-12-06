import time
from typing import Optional, List
from fastapi import APIRouter, Cookie, Form, Header
from custom_log import log
from fastapi.responses import PlainTextResponse, Response, HTMLResponse
router = APIRouter(
  prefix='/product',
  tags=['product']
)
product = ['watch','camera','phone']
async def time_consuming_functionality():
  time.sleep(5)
  return 'ok'

@router.get('/all')
async def get_all_products():
  await time_consuming_functionality()
  log("myAPI", "Call to get all products")
  # return product   # JSON response
  data  = " ".join(product)
  response = Response(content=data, media_type='text/plain')
  response.set_cookie(key="test_cookie", value="test_cookie_value")
  # return Response(content=data, media_type='text/plain')  #custom response
  return response

# why?
# add parameters: headers , cookies
# different type of response -> plain text, HTML, XML, files, streaming
# complex decisional logic -> give us the opportunity to choose when and how we return our response
# better docs

@router.get('/{id}', responses={
  200:{
    "content": {
      "text/html":{
        "eample":"<div>poduct</div>"
      }
    },
    "description": "Returns HTML for an object"
  },
  404:{
        "content": {
      "text/plain":{
        "example":"product not available"
      }
    },
    "description": "a clear text error message"
  }
})
def get_product(id: int):
  if id > len(product):
    out = "product not available"
    return PlainTextResponse(status_code=404,content=out, media_type='text/plain')
  else:
    product = product[id]
    out = """
  <head>
    <style>
      .product{{
        width: 500px;
        height: 30px;
        border: 2px insert green;
        background-color: lightblue;
        text-align: center;
      }}
    </style>
  </head>
  <div class="product">{product}</div>
  """
    return HTMLResponse(content=out, media_type='text/html')

# headers = are pieces of information that are transmitted with the request and received with the response, so we can manuplate both the request headers and the response header in the fastAPI
@router.get('/withheader')
# def get_products(response: Response, custom_header:Optional[str] = Header(None)):
def get_products(response: Response, custom_header:Optional[List[str]] = Header(None), test_cookie: Optional[str] = Cookie(None)):
  if custom_header:
    response.headers['custom-response-header'] = ", ".join(custom_header)
  return {
    'data': product,
    'custom_header': custom_header,
    'my_cookie': test_cookie
  }

# cookies -> are used to store information on the browser, can accept list, str, dict, models etc (in get_all function and in get_products)
# form data : reteriving data from forms to fill
@router.post('/new')
def create_product(name: str = Form(...)):
  product.append(name)
  return product

# CORS -> Cross Origin Resource Sharing -> means that we are not allowed to access resources on the same meachine based on different endpoints, based on different paths (eg, loacalhost:8080 <..> localhost:8000)
# app.add_middleware(
#   CORSMiddleware, 
#   allow_origins=['https://localhost:3000'],  # eg.
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"]
# )
