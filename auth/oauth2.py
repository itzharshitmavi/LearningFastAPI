from email import header
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db import db_user
from db.database import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'E9987D46064D82929E109BD4265AF23F3CBE71F3964581F5A31B798163389991'
# openssl rand -hex 32 # terminal command to generate random keys in cmd in project folder selection
# or
# import secrets
# print(secrets.token_hex(32))
# in powershell -> [System.BitConverter]::ToString((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }) -as [byte[]]).Replace('-', '')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
  credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials', headers={"www-Authenticate": "Bearer"})
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exceptions
  except JWTError:
    raise credentials_exceptions
  
  user = db_user.get_user_by_username(db, username)
  if user is None:
    raise credentials_exceptions
  return user