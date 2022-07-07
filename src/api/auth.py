from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from . import models, schemas, settings
from .crud import get_user
from .dependencies import get_db
from .exceptions import HttpUnauthorized, RecordNotFoundError

auth_router = APIRouter()


def authenticate_user(db: Session, email: str, password: str) -> models.UserModel:
    try:
        user = get_user(db, email)
    except RecordNotFoundError:
        raise HttpUnauthorized('Incorrect username or password')
    if not settings.pwd_context.verify(password, user.hashed_password):
        raise HttpUnauthorized('Incorrect username or password')
    return user


def create_access_token(**payload_data):
    to_encode = payload_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@auth_router.post("/token", response_model=schemas.Token)
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(sub=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
