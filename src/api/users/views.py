from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from api.dependencies import get_db

from .models import UserInput, UserOutput
from .queries import create_user

users_router = APIRouter(prefix='/user')


@users_router.post('/sign_up', status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def sign_up(user: UserInput = Body(), db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except IntegrityError as error:
        email = error.params['email']
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email {email} already exists',
        )
