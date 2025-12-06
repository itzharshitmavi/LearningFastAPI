from custom_log import log
from fastapi import APIRouter, Depends
from fastapi.requests import Request
router = APIRouter(
  prefix='/dependencies',
  tags=['dependencies'],
  dependencies=[Depends(log)]
)
# multi level dependencies -> dependencies can have dependecies
def convert_params(request: Request, sepereator: str):
  query = []
  for key, value in request.query_params.items():
     query.append(f"{key} {sepereator} {value}")
  return query

#simple dependency

def convert_headers(request: Request, Separator: str='--', query = Depends(convert_params)):
# def convert_headers(request: Request, Seperator: str='--'):
  out_headers = []
  for key, value in request.headers.items():
    # out_headers.append(f"{key} -- {value}")
        out_headers.append(f"{key} {Separator} {value}")
  # return out_headers
  return{
     'headers': out_headers,
     'query': query
  }

@router.get('')
# def get_items(headers = Depends(convert_headers)):
# def get_items(test: str,separator: str = '--',headers = Depends(convert_headers)):
def get_items(separator: str = '--',headers = Depends(convert_headers)):
  return{
    'items': ['a','b','c'],
    'headers': headers
  }
@router.post('/new')
def create_items(headers = Depends(convert_headers)):
  return{
    'result': 'new item created',
    'headers': headers
  }

# class dependencies -> any callable can be a dependency
class Account:
  def __init__(self, name: str, email: str):
    self.name = name
    self.email = email

@router.post('/user')
def create_user(name: str, email: str, password: str, account: Account = Depends(Account)):
  return{
    'name': account.name,
    'email': account.email
  }

# global dependency -> apply to *all endpoints
# can be apply to both router and app

