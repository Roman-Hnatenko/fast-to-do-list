from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserInput(UserBase):
    password: str = Field()


class UserOutput(UserBase):
    id: int

    class Config:
        orm_mode = True
