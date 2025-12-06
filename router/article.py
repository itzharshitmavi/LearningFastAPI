from fastapi import APIRouter, Depends
from schemas import UserBase, articleDisplay, aricleBase
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_article
from typing import List
from auth.oauth2 import get_current_user, oauth2_schema
router = APIRouter(
  prefix='/article',
  tags={'article'}
)
# create article
@router.post('/', response_model=articleDisplay)
def create_article(request: aricleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
  return db_article.create_article(db, request)

# get specific article
# @router.get('/{id}', response_model = articleDisplay)
# def get_article(id: int, db: Session = Depends(get_db), token:str = Depends(oauth2_schema)):
#   return db_article.get_article(db, id)

@router.get('{id}')
def get_article(id: int, db: Session = Depends(get_db), current_user: UserBase =  Depends(get_current_user)):
  return{
    'data': db_article.get_article(db, id),
    'current_user': current_user
  }
