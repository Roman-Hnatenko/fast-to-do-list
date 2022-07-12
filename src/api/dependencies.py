
from datetime import timedelta
from typing import AsyncGenerator

from aioredis import Redis
from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db_models import UserModel

from . import settings
from .database import async_session
from .exceptions import HttpUnauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis = await Redis(decode_responses=True)
    yield redis
    await redis.close()


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


async def add_user_to_redis(redis: Redis, user: UserModel):
    data = jsonable_encoder(user)
    await redis.hmset(user.email, data)
    await redis.expire(user.email, timedelta(minutes=10))


async def get_current_user(
    background_tasks: BackgroundTasks,
    email: str = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> UserModel:
    if cached_user := await redis.hgetall(email):
        cached_user['id'] = int(cached_user['id'])
        return UserModel(**cached_user)
    result = await session.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar()
    background_tasks.add_task(add_user_to_redis, redis, user)
    return user
