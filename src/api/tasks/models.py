from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    title: str
    description: str


class TaskOutput(TaskInput):
    id: int
    create_at: str
    finished_at: str = Field(default=None)

    class Config:
        orm_mode = True


class TaskToUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    finished_at: str | None = None
