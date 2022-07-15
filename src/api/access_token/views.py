from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from api import settings
from db_models import UserModel
from api.dependencies import get_session
from api.exceptions import HttpUnauthorized

from .models import Token
from .queries import get_user

auth_router = APIRouter()


async def authenticate_user(session: AsyncSession, email: str, password: str) -> UserModel:
    try:
        user = await get_user(session, email)
    except NoResultFound:
        raise HttpUnauthorized('Incorrect username or password')
    if not settings.pwd_context.verify(password, user.hashed_password):
        raise HttpUnauthorized('Incorrect username or password')
    return user


def create_access_token(**payload_data):
    to_encode = payload_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@auth_router.post('/token', response_model=Token)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    access_token = create_access_token(sub=user.email)
    return {'access_token': access_token, 'token_type': 'bearer'}
