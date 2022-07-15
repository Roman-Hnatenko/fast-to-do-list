from datetime import datetime

from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    title: str
    description: str
    priority: int = Field(default=0)


class TaskOutput(TaskInput):
    id: int
    created_at: datetime
    finished_at: datetime | None = None

    class Config:
        orm_mode = True


class TaskToUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    finished_at: datetime | None = None
    priority: int | None = None
