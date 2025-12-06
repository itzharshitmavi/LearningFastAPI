from fastapi import HTTPException, status
from db.models import dbArticle
from exceptions import storyException
from schemas import aricleBase
from sqlalchemy.orm.session import Session
def create_article(db: Session, request: aricleBase):
  if request.content.startswith('once upon a time'):
    raise storyException('no stories please')
  new_article = dbArticle(
    title = request.title,
    content = request.content,
    published = request.published, 
    user_id = request.creator_id
  )
  db.add(new_article)
  db.commit()
  db.refresh(new_article)
  return new_article

def get_article(db: Session, id: int):
  article = db.query(dbArticle).filter(dbArticle.id == id).first()
  if not article:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f'Article with id {id} not found'))
  return article