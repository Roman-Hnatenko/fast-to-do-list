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


class TaskInput(BaseModel):
    title: str
    description: str


class TaskOutput(TaskInput):
    id: int
    create_at: str
    finished_at: str = Field(default=None)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
