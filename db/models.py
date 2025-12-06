from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
class  DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  items = relationship("dbArticle", back_populates='user')
class dbArticle(Base):
  __tablename__ = 'aritcles'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  content = Column(String)
  published = Column(Boolean)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("DbUser", back_populates='items')