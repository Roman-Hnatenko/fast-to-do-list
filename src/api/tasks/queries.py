from sqlalchemy.orm import Session

from api.db_models import TaskModel
from api.exceptions import RecordNotFoundError

from .models import TaskInput, TaskToUpdate


def get_task(db: Session, task_id: str):
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()


def save_task(db: Session, task: TaskInput, user_id: int) -> TaskModel:
    db_task = TaskModel(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_from_db(db: Session, id: int, user_id: int) -> TaskModel:
    if task := db.query(TaskModel).filter(TaskModel.id == id, TaskModel.owner_id == user_id).first():
        return task
    raise RecordNotFoundError()


def delete_task_from_db(db: Session, id: int, user_id: int):
    db.query(TaskModel).filter(TaskModel.id == id, TaskModel.owner_id == user_id).delete()
    db.commit()


def update_task_in_db(db: Session, id: int, task: TaskToUpdate, user_id: int):
    query = db.query(TaskModel).filter(TaskModel.id == id, TaskModel.owner_id == user_id)
    if items := query.first():
        query.update(task.dict(exclude_unset=True))
        db.commit()
        return items
    raise RecordNotFoundError()
