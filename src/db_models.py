from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


def get_current_utc_time() -> datetime:
    return datetime.now(tz=timezone.utc)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    # priority = Column(Integer, default=0)
    tasks = relationship('TaskModel', back_populates='owner')


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=get_current_utc_time)
    finished_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('UserModel', back_populates='tasks')
