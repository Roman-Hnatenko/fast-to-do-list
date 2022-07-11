
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db_models import UserModel

from . import settings
from .database import async_session
from .exceptions import HttpUnauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def require_auth(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HttpUnauthorized('Could not validate credentials')
    email: str = payload.get('sub')
    if not email:
        raise HttpUnauthorized('Could not validate credentials')
    return email


async def get_current_user(
    email: str = Depends(require_auth), session: AsyncSession = Depends(get_session),
) -> UserModel:
    result = await session.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar()
