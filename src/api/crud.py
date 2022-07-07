from sqlalchemy.orm import Session

from .exceptions import RecordNotFoundError
from .models import TaskModel, UserModel
from .schemas import TaskInput, UserInput
from .settings import pwd_context


def get_task(db: Session, task_id: str):
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()


def get_user(db: Session, email: str) -> UserModel:
    if ddb_user := db.query(UserModel).filter(UserModel.email == email).first():
        return ddb_user
    raise RecordNotFoundError()


def create_user(db: Session, user: UserInput) -> UserModel:
    db_user = UserModel(
        email=user.email,
        name=user.name,
        hashed_password=pwd_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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


def update_task_in_db(db: Session, task_id: int, fields_to_update, user_id: int):
    db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.owner_id == user_id).update()
