from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session

from .models import UserInput, UserOutput
from .queries import create_user

users_router = APIRouter(prefix='/user')


@users_router.post('/sign_up', status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def sign_up(user: UserInput = Body(), session: AsyncSession = Depends(get_session)):
    try:
        return await create_user(session, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {user.email} already exists',
        )
