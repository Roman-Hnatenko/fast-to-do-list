from datetime import datetime, timezone
from uuid import uuid1

from sqlalchemy import DATETIME, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, default=uuid1)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, default=uuid1)
    title = Column(String)
    description = Column(String)
    create_at = Column(DATETIME, default=datetime.now(tz=timezone.utc))
    finished_at = Column(DATETIME)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
