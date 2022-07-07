from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from .crud import create_user
from .dependencies import get_db
from .schemas import UserInput, UserOutput

users_router = APIRouter()


@users_router.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def sign_in(user: UserInput = Body(), db: Session = Depends(get_db)):
    return create_user(db, user)
