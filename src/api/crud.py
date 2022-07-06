from sqlalchemy.orm import Query, Session

from . import models, schemas


def get_task(db: Session, task_id: str) -> Query:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_user(db: Session, user_id: str) -> Query:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, task: schemas.User) -> models.User:
    db_user = models.Task(**task.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_task(db: Session, task: schemas.Task, user_id: str) -> models.Task:
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
