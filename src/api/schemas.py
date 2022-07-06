from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

# class User(BaseModel):
#     id: UUID
#     username: str
#     email: EmailStr


class Task(BaseModel):
    title: str
    description: str
    create_at: datetime
    finished_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
