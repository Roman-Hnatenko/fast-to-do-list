
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api.ddb_models import UserModel

from . import settings
from .database import SessionLocal
from .exceptions import HttpUnauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def require_auth(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HttpUnauthorized('Could not validate credentials')
    email: str = payload.get("sub")
    if not email:
        raise HttpUnauthorized('Could not validate credentials')
    return email


async def get_current_user(email: str = Depends(require_auth), db: Session = Depends(get_db)) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()
